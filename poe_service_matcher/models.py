from datetime import datetime
from sqlalchemy import UniqueConstraint

from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(90), unique = True, nullable = False)

    services = db.relationship('ServiceListing', backref='user', lazy = True)

    def __repr__(self):
        return f'ServiceListing(user_id={self.user_id}, service={self.service})'

class ServiceListing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)   
    service = db.Column(db.String(90), unique = False, nullable = False)

    map_provided = db.Column(db.Boolean, default=False, nullable = True)
    
    slots = db.Column(db.Integer, unique = False, nullable = True, default = 1)
    
    price = db.Column(db.Integer, unique = False, nullable = True)

    time_listed = db.Column(db.DateTime, default = datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'service', name='_user_service_uc'),)	

    def __repr__(self):
        return f'ServiceListing(user_id={self.user_id}, service={self.service})'


