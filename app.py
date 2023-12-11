# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask
from flask import jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
MS = Base.classes.measurement
ST = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f'/api/v1.0/[start]<br/>'
        f'/api/v1.0/[start]/[end]'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():   
    results = session.query(MS.date, MS.prcp).filter(MS.date>='2016-08-23').all()
    return jsonify({d:p for d,p in results})
    session.close()

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(MS.station).all()
    stations = {s for s, in results}
    return jsonify(list(stations))
    session.close()

@app.route('/api/v1.0/tobs')
def tobs():
    station = 'USC00519281'
    sel = [MS.station, MS.tobs, MS.date]
    active_station = session.query(*sel).filter(MS.date > '2016-08-22').filter((MS.station) == station).all()
    active = [{'station': a, 'tobs': b, 'date': c} for a, b, c in active_station]
    return jsonify(active)
    session.close()