from app import app, logfile
from datetime import datetime

def pdebug(message):
    if app.env == "development":
        print(message)
    if app.config["LOG"]:
        logfile.write(f"[{datetime.now()}]  {message}\n")
        logfile.flush()
