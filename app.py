from flask import Flask, jsonify
from models import db, connect_db
import os 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'some secreet'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('ENV_VAR_NAME', 'postgresql:///capstone_1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

