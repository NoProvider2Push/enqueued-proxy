from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
import os
import atexit

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
logfile = open(Config.LOG_FILE, "a")
cron = BackgroundScheduler(daemon = True)
cron.start()

from app import routes, models, queue
from app.utils import pdebug

if (not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true") and not os.path.exists(Config.LOCK):
    pdebug("Add cron")
    f = open(Config.LOCK,"wb")
    f.write(b"locked")
    f.close()
    cron.add_job(queue.try_again, "interval", seconds=Config.TRY_AGAIN_TIMEOUT).modify(max_instances=Config.MAX_TRY_AGAIN_INSTANCES)
    cron.add_job(queue.purge, "interval", seconds=Config.PURGE_TIMEOUT)

@atexit.register
def remove_lock():
    print("Exit: Removing lock")
    if os.path.isfile(Config.LOCK):
        os.remove(Config.LOCK)

from app import routes, models
