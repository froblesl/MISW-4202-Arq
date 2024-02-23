from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, event

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db?mode=locking=normal'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return app