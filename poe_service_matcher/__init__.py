from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from .models import User, ServiceListing

@app.route('/')
def index():
    services = ServiceListing.query.all()
    return render_template('index.html', services=services)