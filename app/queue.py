from app import app, db
from app.utils import pdebug
from app.models import Distributor, Message
from config import Config
from threading import Thread
from datetime import datetime
import requests
requests.urllib3.disable_warnings()

def add(ip, port, uri, message):
    pdebug(f"Add pending message to {ip}")
    distrib = Distributor.query.filter_by(ip=ip).first()
    if not distrib:
        pdebug("New pending distrib")
        distrib = Distributor(ip=ip, port=port)
        db.session.add(distrib)
    if (len(distrib.messages.all()) > Config.N_MAX_MESSAGES):
        return False
    message = Message(uri=uri, content=message, distributor=distrib)
    db.session.add(message)
    db.session.commit()
    return True

def try_again():
    pdebug("try_again")
    for d in Distributor.query.all():
        pdebug(f"trying {d.ip}")
        try:
            rep = requests.get(
                f"http://{d.ip}:{d.port}/",
                timeout=1
            )
            if rep.ok and rep.content == b"ok":
                for m in d.messages:
                    resend_async(d.ip, d.port, m.uri, m.content)
                if d.messages.all() == []:
                    pdebug(f"Remove pending distrib {d.ip}")
                    db.session.delete(d)
                db.session.commit()
        except:
            pass
    return True

def purge():
    pdebug("purge")
    now = datetime.now()
    for m in Message.query.all():
        if (( now - m.timestamp ).total_seconds() > app.config["PURGE_TIMEOUT"]):
            pdebug(f"Removing message {m.id}")
            db.session.delete(m)
    for d in Distributor.query.all():
        if d.messages.all() == []:
            pdebug(f"Removing Distrib {d.ip}")
            db.session.delete(d)
    db.session.commit()
    
    return True

def send(ip, port, uri, message):
    pdebug(f"send to {ip}:{port}/{uri}")
    try:
        rep = requests.post(
            f"http://{ip}:{port}/{uri}",
            data = message,
            timeout = app.config["REQ_TIMEOUT"]
        )
        if rep.ok and rep.content == b"ok":
            return True
    except:
        pass
    pdebug(f"Cannot send to {ip}")
    add(ip, port, uri, message)

def send_async(ip, port, uri, message):
    pdebug(f"send_async to {ip}:{port}/{uri}")
    thread = Thread(target=send, args=(
        ip,
        port,
        uri,
        message
    ))
    thread.daemon = True
    thread.start()

def resend(distrib, message):
    pdebug(f"resend to {distrib.ip}:{distrib.port}/{message.uri}")
    try:
        rep = requests.post(
            f"http://{distrib.ip}:{distrib.port}/{message.uri}",
            data = message.content,
            timeout = app.config["REQ_TIMEOUT"]
        )
        if rep.ok and rep.content == b"ok":
            pdebug(f"remove pending message to {message.uri}")
            db.session.delete(message)
            return True
    except:
        pass
    pdebug(f"Cannot send to {ip}")
    add(ip, port, uri, message)

def resend_async(distrib, message):
    pdebug(f"resend to {distrib.ip}:{distrib.port}/{message.uri}")
    thread = Thread(target=resend, args=(
        distrib,
        message
    ))
    thread.daemon = True
    thread.start()
