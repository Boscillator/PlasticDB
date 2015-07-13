"""
Web Routes
"""
from Server import app, db
from Server.models import *
from flask import render_template, request, redirect, url_for
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

@app.route('/sample/<int:id>')
def sample(id):
    s = Sample.query.filter_by(id=id).first()
    return str(s.events)