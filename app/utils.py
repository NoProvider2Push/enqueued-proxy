from app import app

def pdebug(message):
    if app.env == "development":
        print(message)
