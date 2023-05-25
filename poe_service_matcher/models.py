from . import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(90), unique = True, nullable = False)

    services = db.relationship('ServiceListing', backref='user', lazy = True)

    def __repr__(self):
        return 'User %r' % self.username

class ServiceListing(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key = True)   
    service = db.Column(db.String(90), unique = False, nullable = False, primary_key = True)

    map_provided = db.Column(db.Boolean, default=False, nullable = True)
    
    slots = db.Column(db.Integer, unique = False, nullable = True, default = 1)
    
    price = db.Column(db.Integer, unique = False, nullable = True)

    time_listed = db.Column(db.DateTime, default = datetime.utcnow)


