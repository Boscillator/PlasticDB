"""
Web Routes
"""
from Server import app, db
from Server.models import *
from flask import render_template, request, redirect, url_for, Response, session, g, abort, flash
import datetime

@app.errorhandler(401)
def handle_UnAuthorized(e):
    flash("You are unauthorized to perform that action")
    return redirect(url_for('samples'))

@app.before_request
def cheackAuth():
    g.auth = 'username' in session

#Login Route
@app.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in app.config['Users'].keys():
        if password == app.config['Users'][username]:
            flash('Login Successful')
            session['username'] = username
        else:
            flash('Invalide password')
    else:
        flash('Invalide username')
            
    return redirect(url_for('samples'))
    
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('samples'))

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
        if not g.auth:
            abort(401)
        #Gets values from form
        CreatedBy = session['username']
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
        Irradiation_Date_MMDDYYYY = request.form['Irradiation_Date_MMDDYYYY']
        Current_Location = request.form['Current_Location']
        
        
        s = Sample(CreatedBy,Row,Material,Doping_Rate,Code_ID,Size_cm,Dose_Mrad,Dose_Rate_Mradhr,Radiation_Source,Atmosphere,Color,Wire_Attached,Irradiation_Date_MMDDYYYY,Current_Location) #Creates sample object
        
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
        if not g.auth:
            abort(401)
        #gets values from form
        CreatedBy = session['username']
        time = request.form['time']
        History_time = request.form['History_time']
        Measurement_type = request.form['Measurement_type']
        sample_number = request.form['sample_number']
        sample_face = request.form['sample_face']
        E_sample_angle = request.form['E_sample_angle']
        E_Excitation_wavelength_nm = request.form['E_Excitation_wavelength_nm']
        E_Excitation_Slit_nm = request.form['E_Excitation_Slit_nm']
        E_Increment_nm = request.form['E_Increment_nm']
        E_Emission_Slit_nm = request.form['E_Emission_Slit_nm']
        A_Baseline_reference = request.form['A_Baseline_reference']
        A_Scan_range_nm = request.form['A_Scan_range_nm']
        A_Spectral_bandwidth_nm = request.form['A_Spectral_bandwidth_nm']
        A_Increment_nm = request.form['A_Increment_nm']
        
        e = Event(CreatedBy,datetime.datetime.now(),History_time , Measurement_type,sample_number,sample_face,E_sample_angle,E_Excitation_wavelength_nm,E_Excitation_Slit_nm,E_Increment_nm, E_Emission_Slit_nm,A_Baseline_reference,A_Scan_range_nm,A_Spectral_bandwidth_nm,A_Increment_nm, s) #create event object
        
        #add and commit to db
        db.session.add(e)
        db.session.commit()
        
        
        return redirect(url_for('event',id=e.id))   #redirect to new events page
    elif request.method == 'GET':
        return render_template('events.html', sample=s)

@app.route('/sample_history/<int:id>', methods=['GET','POST'])
def sample_history(id):
    """
        Gets history of a sample
        Post creates new history under this sample
        """
    s = Sample.query.filter_by(id=id).first()   #gets current sample from db
    
    #breadcrumb stuff
    session['sample'] = id
    session.pop('history',None)
    
    if request.method == 'POST':
        if not g.auth:
            abort(401)
        #gets values from form
        CreatedBy = session['username']
        Date = request.form['Date']
        Location = request.form['Location']
        Note = request.form['Note']
        
        h = History(CreatedBy,Date,Location,Note,s) #create history object
        
        #add and commit to db
        db.session.add(h)
        db.session.commit()
        
        
        return render_template('histories.html', sample=s)   #Return this template, no reason to redirect
    elif request.method == 'GET':
        return render_template('histories.html', sample=s)

@app.route('/sample/<int:id>/delete')
def deleteSample(id):
    if not g.auth:
            abort(401)
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
        if not g.auth:
            abort(401)
        f = request.files['file']   #get files as filetype object from database
        data = f.read()
        CreatedBy = session['username']
        Notes = request.form['Notes']
        m = Mesurement(CreatedBy,data,Notes,e)  #create messurement
        
        #add to db
        db.session.add(m)
        db.session.commit()
        
        return render_template('messurments.html', event = e)   #Return this template, no reson to redirect
    elif request.method == 'GET':
        return render_template('messurments.html', event = e)   #Return template

@app.route('/event/<int:id>/delete')
def deleteEvent(id):
    if not g.auth:
            abort(401)
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

@app.route('/mesurement/<int:id>/delete')
def deleteMessurement(id):
    if not g.auth:
            abort(401)
    m = Mesurement.query.filter_by(id=id).first()
    db.session.delete(m)
    db.session.commit()
    return redirect('/')
