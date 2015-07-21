"""
Web Routes
"""
from Server import app, db
from Server.models import *
from flask import render_template, request, redirect, url_for, Response, session
import datetime

@app.route('/')
@app.route('/sample', methods=['GET','POST'])
def samples():
    """
    Returns list of samples on get request and creates sample on post request
    """
    #breadcrumb stuff
    session.pop('sample',None)
    session.pop('event',None)
    
    if request.method == 'POST':
        #Gets values from form
        Row = request.form['Row']
        Material = request.form['Material']
        Doping_Rate = request.form['Doping_Rate']
        Code_ID = request.form['Code_ID']
        Size_cm = request.form['Size_cm']
        Dose_Mrad = request.form['Dose_Mrad']
        Dose_Rate_Mradhr = request.form['Dose_Rate_Mradhr']
        Radiation_Source = request.form['Radiation_Source']
        Atmosphere = request.form['Atmosphere']
        Color = request.form['Color']
        Wire_Attached = request.form['Wire_Attached']
        Location = request.form['Location']
        Irradiation_Date_MMDDYYYY = request.form['Irradiation_Date_MMDDYYYY']
        Notes1 = request.form['Notes1']
        Notes2 = request.form['Notes2']
        
        
        s = Sample(Row,Material,Doping_Rate,Code_ID,Size_cm,Dose_Mrad,Dose_Rate_Mradhr,Radiation_Source,Atmosphere,Color,Wire_Attached,Location,Irradiation_Date_MMDDYYYY,Notes1,Notes2) #Creates sample object
        
        db.session.add(s)   #addes sample to db
        db.session.commit()
        
        return redirect(url_for('sample',id=s.id))  #Redirects to the samples page
        
    elif request.method == 'GET':
        samples = Sample.query.all()    #Gets list of samples from the database
        return render_template("sample.html", samples = samples)    #Renders template

@app.route('/sample/<int:id>', methods=['GET','POST'])
def sample(id):
    """
    Gets events of a sample
    Post creates new event under this sample
    """
    s = Sample.query.filter_by(id=id).first()   #gets current sample from db
    
    #breadcrumb stuff
    session['sample'] = id
    session.pop('event',None)
    
    if request.method == 'POST':
        #gets values from form
        time = request.form['time']
        Measurement_type = request.form['Measurement_type']
        sample_number = request.form['sample_number']
        sample_face = request.form['sample_face']
        sample_angle = request.form['sample_angle']
        Excitation_wavelength_nm = request.form['Excitation_wavelength_nm']
        Excitation_Slit_nm = request.form['Excitation_Slit_nm']
        Increment_nm = request.form['Increment_nm']
        Emission_Slit_nm = request.form['Emission_Slit_nm']
        
        e = Event(datetime.datetime.now(),Measurement_type,sample_number,sample_face,sample_angle,Excitation_wavelength_nm,Excitation_Slit_nm,Increment_nm, Emission_Slit_nm, s) #create event object
        
        #add and commit to db
        db.session.add(e)
        db.session.commit()
        
        
        return redirect(url_for('event',id=e.id))   #redirect to new events page
    elif request.method == 'GET':
        return render_template('events.html', sample=s)
    
@app.route('/sample/<int:id>/delete')
def deleteSample(id):
    s = Sample.query.filter_by(id=id).first()
    
    for event in s.events.all():
        for messurement in event.mesurements.all():
            db.session.delete(messurement)
        db.session.delete(event)
    db.session.delete(s)
    
    db.session.commit()
    
    return redirect('/')

@app.route('/event/<int:id>',methods=['GET','POST'])
def event(id):
    """
    Displayes mesurements of event on GET
    Creates mesurement on POST
    """
    e = Event.query.filter_by(id=id).first()    #get event from db
    
    session['event'] = id
    
    if request.method == 'POST':
        f = request.files['file']   #get files as filetype object from database
        data = f.read()
        Notes = request.form['Notes']
        m = Mesurement(data,Notes,e)  #create messurement
        
        #add to db
        db.session.add(m)
        db.session.commit()
        
        return render_template('messurments.html', event = e)   #Return this template, no reson to redirect
    elif request.method == 'GET':
        return render_template('messurments.html', event = e)   #Return template

@app.route('/event/<int:id>/delete')
def deleteEvent(id):
    e = Event.query.filter_by(id=id).first()
    for messurement in e.mesurements.all():
        db.session.delete(messurement)
    db.session.delete(e)
    db.session.commit()
    return redirect('/')


@app.route('/mesurement/<int:id>')
def messurement(id):
    m = Mesurement.query.filter_by(id=id).first()   #get mesurement by id
    return Response(m.data, mimetype='text/plain')  #Retrun plain text file with mesurments data

@app.route('/messurment/<int:id>/delete')
def deleteMessurement(id):
    m = Mesurement.query.filter_by(id=id).first()
    db.session.delete(m)
    db.session.commit()
    return redirect('/')
