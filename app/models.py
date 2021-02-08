from app import db
from datetime import datetime

class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(64), index=True, unique=True)
    port = db.Column(db.Integer)
    messages = db.relationship("Message", backref="distributor", lazy="dynamic")

    def __repr__(self):
        return '<Distributor {}>'.format(self.ip)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(1024))
    content = db.Column(db.String(4096))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.id)
