# 1. import Flask
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import or_
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

m = Base.classes.measurement
s = Base.classes.station

session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to this shit assignment!"

# 3. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation/")
def home():
    year = dt.date.today() - dt.timedelta(days=365)
    qry = session.query(*[m.date,m.prcp]).filter(m.date >= year).all()
    dic = {}
    for e in qry:
        dic[e[0]] = e[1]
    return jsonify(dic)

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations/")
def about():
    st = session.query(*[m.station]).group_by(m.station).order_by(m.tobs.desc()).all()
    dic2 = {}
    k = 1
    for e in st:
        dic2[k] = e[0]
        k=k+1
    return jsonify(dic2)

@app.route("/api/v1.0/tobs/")
def tobs():
    year = dt.date.today() - dt.timedelta(days=365)
    nd = session.query(*[m.date, m.tobs]).\
        filter(m.date >= year).\
        filter(or_(m.station == 'USC00519281')).\
        all()
    dic3 = {}
    for e in nd:
        dic3[e[0]] = e[1]
    return jsonify(dic3)

@app.route("/api/v1.0/<start>/")
def sas(start):
    def temps(start):
        min_t = session.query(func.min(m.tobs)).\
            filter(m.date >= start).\
            scalar()
        max_t = session.query(func.max(m.tobs)).\
            filter(m.date >= start).\
            scalar()
        mean_t = session.query(func.avg(m.tobs)).\
            filter(m.date >= start).\
            scalar()
        return {"min": min_t,
                "max": max_t,
                "mean": mean_t}
    return jsonify(temps(start))

@app.route("/api/v1.0/temp/<start>/<end>/")
def meh(start,end):
    def calc_temps(start, end):
        min_t = session.query(func.min(m.tobs)).\
            filter(m.date <= end).\
            filter(m.date >= start).\
            scalar()
        max_t = session.query(func.max(m.tobs)).\
            filter(m.date <= end).\
            filter(m.date >= start).\
            scalar()
        mean_t = session.query(func.avg(m.tobs)).\
            filter(m.date <= end).\
            filter(m.date >= start).\
            scalar()
        return {"min": min_t,
                "max": max_t,
                "mean": mean_t}
    return jsonify(calc_temps(start, end))

if __name__ == "__main__":
    app.run(debug=True)