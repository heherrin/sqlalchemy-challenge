# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 05:58:31 2021

@author: heath
"""

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

#define tabels
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/Start_Only<br/>"
        f"/api/v1.0/start_end<br/>"
    )


#Create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    """Return a list of dates and precipitation"""
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    precipitation_data = list(np.ravel(results))

    return jsonify(precipitation_data)


#Create new route to pull station data
@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
    results = session.query(Station.station).all()

    session.close()
    stationslist = list(np.ravel(results))

    return jsonify(stationslist)

#create new route to pull Tobs data
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-24').all()

    session.close()
    
    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)

#create new route to pull temp data based on start date


# run app with debugger off
if __name__ == '__main__':
    app.run(debug=False)
