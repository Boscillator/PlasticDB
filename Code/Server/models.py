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
    Row = db.Column(db.Integer)
    Material = db.Column(db.String(20))
    Doping_Rate = db.Column(db.String(20))
    Code_ID = db.Column(db.String(20))
    Size_cm = db.Column(db.String(30))
    Dose_Mrad = db.Column(db.String(20))
    Dose_Rate_Mradhr = db.Column(db.String(10))
    Radiation_Source = db.Column(db.String(80))
    Atmosphere = db.Column(db.String(80))
    Color = db.Column(db.String(80))
    Wire_Attached = db.Column(db.String(80))
    Location = db.Column(db.String(20))
    Irradiation_Date_MMDDYYYY = db.Column(db.String(30))
    Notes1 = db.Column(db.String(500))
    Notes2 = db.Column(db.String(500))
    
    def __init__(self, Row, Material, Doping_Rate, Code_ID, Size_cm, Dose_Mrad, Dose_Rate_Mradhr, Radiation_Source, Atmosphere, Color, Wire_Attached, Location, Irradiation_Date_MMDDYYYY, Notes1, Notes2):
        self.Row = Row
        self.Material = Material
        self.Doping_Rate = Doping_Rate
        self.Code_ID = Code_ID
        self.Size_cm = Size_cm
        self.Dose_Mrad = Dose_Mrad
        self.Dose_Rate_Mradhr = Dose_Rate_Mradhr
        self.Radiation_Source = Radiation_Source
        self.Atmosphere = Atmosphere
        self.Color = Color
        self.Wire_Attached = Wire_Attached
        self.Location = Location
        self.Irradiation_Date_MMDDYYYY = Irradiation_Date_MMDDYYYY
        self.Notes1 = Notes1
        self.Notes2 = Notes2


class Event(db.Model):
    """
    Model used for event
    Referse to Sample
    """
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    History_time = db.Column(db.String(30))
    Measurement_type = db.Column(db.String(30))
    sample_number = db.Column(db.Integer)
    sample_face = db.Column(db.String(10))
    E_sample_angle = db.Column(db.String(10))
    E_Excitation_wavelength_nm = db.Column(db.String(20))
    E_Excitation_Slit_nm = db.Column(db.String(20))
    E_Increment_nm = db.Column(db.String(20))
    E_Emission_Slit_nm = db.Column(db.String(20))
    A_Baseline_reference = db.Column(db.String(30))
    A_Scan_range_nm = db.Column(db.String(50))
    A_Spectral_bandwidth_nm = db.Column(db.String(10))
    A_Increment_nm = db.Column(db.String(10))
    
    
    sample_ID = db.Column(db.Integer, db.ForeignKey('sample.id'))
    sample = db.relationship('Sample', backref=db.backref('events', lazy='dynamic'))
    
    def __init__(self,time,History_time,Measurement_type,sample_number,sample_face,E_sample_angle,E_Excitation_wavelength_nm,E_Excitation_Slit_nm,E_Increment_nm,E_Emission_Slit_nm,A_Baseline_reference,A_Scan_range_nm,A_Spectral_bandwidth_nm,A_Increment_nm,sample):
        self.time = time
        self.History_time = History_time
        self.Measurement_type = Measurement_type
        self.sample_number = sample_number
        self.sample_face = sample_face
        self.E_sample_angle = E_sample_angle
        self.E_Excitation_wavelength_nm = E_Excitation_wavelength_nm
        self.E_Excitation_Slit_nm = E_Excitation_Slit_nm
        self.E_Increment_nm = E_Increment_nm
        self.E_Emission_Slit_nm = E_Emission_Slit_nm
        self.A_Baseline_reference = A_Baseline_reference
        self.A_Scan_range_nm = A_Scan_range_nm
        self.A_Spectral_bandwidth_nm = A_Spectral_bandwidth_nm
        self.A_Increment_nm = A_Increment_nm
        self.sample = sample
    
class Mesurement(db.Model):
    """
    Model used for a Mesurement
    Stores mesurment text file
    Referse to Event
    """
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.LargeBinary)
    Notes = db.Column(db.String(500))
    
    event_ID = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship('Event', backref=db.backref('mesurements',lazy='dynamic'))
    
    def __init__(self, data, Notes, event):
        self.data = data
        self.Notes = Notes
        self.event = event