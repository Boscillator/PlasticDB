"""
SQL models
"""

from Server import db
from datetime import datetime

class Sample(db.Model):
    """
    Model used for plastic sample
    """
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    plasticType = db.Column(db.String(10))
    fiberType = db.Column(db.String(80))
    fiberDiamiter = db.Column(db.String(80))
    
    def __init__(self, time, plasticType, fiberType, fiberDiamiter):
        self.time = time
        self.plasticType = plasticType
        self.fiberType = fiberType
        self.fiberDiamiter = fiberDiamiter
    



class Event(db.Model):
    """
    Model used for event
    Referse to Sample
    """
    id = db.Column(db.Integer, primary_key=True)
    dose = db.Column(db.String(10))
    temperature = db.Column(db.String(10))
    atmosType = db.Column(db.String(10))
    
    sample_ID = db.Column(db.Integer, db.ForeignKey('sample.id'))
    sample = db.relationship('Sample', backref=db.backref('events', lazy='dynamic'))
    
    def __init__(self,dose, temperature, atmosType, sample):
        self.dose = dose
        self.temperature = temperature
        self.atmosType = atmosType
        self.sample = sample
    
class Mesurement(db.Model):
    """
    Model used for a Mesurement
    Stores mesurment text file
    Referse to Event
    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)
    
    event_ID = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship('Event', backref=db.backref('events',lazy='dynamic'))
    
    def __int__(self, data, event):
        self.data = data
        self.event = event