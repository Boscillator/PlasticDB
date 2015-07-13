"""
Web Routes
"""
from Server import app, db
from Server.models import *
from flask import render_template, request, redirect, url_for, Response
import datetime

@app.route('/')
@app.route('/sample', methods=['GET','POST'])
def samples():
    if request.method == 'POST':
        plasticType = request.form['plasticType']
        fiberType = request.form['fiberType']
        fiberDiamiter = request.form['fiberDiamiter']
        s = Sample(datetime.datetime.now(),plasticType,fiberType,fiberDiamiter)
        db.session.add(s)
        db.session.commit()
        return redirect(url_for('sample',id=s.id))
        
    elif request.method == 'GET':
        samples = Sample.query.all()
        return render_template("sample.html", samples = samples)    

@app.route('/sample/<int:id>', methods=['GET','POST'])
def sample(id):
    s = Sample.query.filter_by(id=id).first()
    
    if request.method == 'POST':
        dose = request.form['dose']
        temperature = request.form['temperature']
        atmosType = request.form['atmosType']
        e = Event(dose,temperature,atmosType,s)
        db.session.add(e)
        db.session.commit()
        return 'done'
    elif request.method == 'GET':
        return render_template('events.html', sample=s)

@app.route('/event/<int:id>',methods=['GET','POST'])
def event(id):
    e = Event.query.filter_by(id=id).first()
    if request.method == 'POST':
        f = request.files['file']
        data = f.read()
        m = Mesurement(data,e)
        db.session.add(m)
        db.session.commit()
        return 'done'
    elif request.method == 'GET':
        return render_template('messurments.html', event = e)
    
@app.route('/mesurement/<int:id>')
def messurement(id):
    m = Mesurement.query.filter_by(id=id).first()
    return Response(m.data, mimetype='text/plain')
    
    
