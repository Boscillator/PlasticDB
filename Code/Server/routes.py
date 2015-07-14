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
        plasticType = request.form['plasticType']
        fiberType = request.form['fiberType']
        fiberDiamiter = request.form['fiberDiamiter']
        primary_dopant_concentration = request.form['primary_dopant_concentration']
        secondary_dopant_concentration = request.form['secondary_dopant_concentration']
        tag = request.form['tag']
        
        s = Sample(datetime.datetime.now(),plasticType,fiberType,fiberDiamiter,primary_dopant_concentration,secondary_dopant_concentration,tag) #Creates sample object
        
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
        dose = request.form['dose']
        temperature = request.form['temperature']
        atmosType = request.form['atmosType']
        
        e = Event(dose,temperature,atmosType,s) #create event object
        
        #add and commit to db
        db.session.add(e)
        db.session.commit()
        
        return redirect(url_for('event',id=e.id))   #redirect to new events page
    elif request.method == 'GET':
        return render_template('events.html', sample=s)

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
        m = Mesurement(data,e)  #create messurement
        
        #add to db
        db.session.add(m)
        db.session.commit()
        
        return render_template('messurments.html', event = e)   #Return this template, no reson to redirect
    elif request.method == 'GET':
        return render_template('messurments.html', event = e)   #Return template
    
@app.route('/mesurement/<int:id>')
def messurement(id):
    m = Mesurement.query.filter_by(id=id).first()   #get mesurement by id
    return Response(m.data, mimetype='text/plain')  #Retrun plain text file with mesurments data
    
