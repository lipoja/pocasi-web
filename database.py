import datetime
import json
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
with open(os.path.join(os.path.dirname(__file__), 'pocasi_db.json')) as dbconf:
    db = json.loads(dbconf.read())

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=db['user'], pw=db['pw'], url=db['url'], db=db['db'])
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    time = db.Column(db.TIMESTAMP,  nullable=False, default=datetime.datetime.now)
