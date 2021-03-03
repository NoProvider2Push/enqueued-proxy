import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # ALLOWED_IP must be equal to "all" or a string array of IP
    # ALLOWED_IP = "all"
    ALLOWED_IP = [ "10.10.10.1" ]
    # ALLOWED_IP must be equal to "all" or an int array of ports
    # ALLOWED_PORTS = "all"
    ALLOWED_PORTS = [ 51515 ]
    # N_MAX messages to keep per IP
    N_MAX_MESSAGES = 100 
    TRY_AGAIN_TIMEOUT = 30 # sec
    PURGE_TIMEOUT = 6 * 60 * 60 # sec, 6h
    REQ_TIMEOUT = 10
    MAX_TRY_AGAIN_INSTANCES = 1
    LOCK = os.path.join(basedir, "lock")
    LOG = True # Verbose !
    LOG_FILE = os.path.join(basedir, 'np2p.log')
