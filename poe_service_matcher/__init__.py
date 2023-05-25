from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder = 'templates')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

from .database import db
from .models import User, ServiceListing

db.init_app(app)

@app.route('/')
def index():
    services = ServiceListing.query.all()
    return render_template('index.html', services=services)