from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
import os

app = Flask(__name__, template_folder = '../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
with app.app_context():
    Session = sessionmaker(bind=db.engine)
    session_factory = scoped_session(Session)

from .models import User, ServiceListing

@app.route('/')
def index():

    session = session_factory()

    services = session.query(ServiceListing).all()

    session.close()
    return render_template('index.html', services=services)

