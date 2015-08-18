"""
Inizilization file for Server
Makes flask app and db
"""
#Imports
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.secret_key = 'DEV'
db = SQLAlchemy(app)

app.config['Users'] = {
    'Fred':'passwordpasswordpassword',
    'OtherUser':'potato'
}

#Import models and routes
import models
import routes