from app import app
from app.queue import send_async
from app.utils import pdebug
from config import Config
from flask import request 

@app.route("/<ip>:<port>/<path:uri>", methods=["GET","POST"])
def proxy(ip, port, uri):
    if request.method == "GET":
        pdebug("Routes: get")
        return "{}"
    if not (
        (ip in Config.ALLOWED_IP or Config.ALLOWED_IP == "all")
        and (int(port) in Config.ALLOWED_PORTS or Config.ALLOWED_PORTS == "all")
    ):
        pdebug("Routes: not allowed")
        return "{}"
    message=request.get_data()
    send_async(ip, port, uri, message)
    return "{}"

