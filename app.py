# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask
from flask import jsonify
from datetime import datetime

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
app.debug = True 
if __name__ == "__main__":
    app.run()


#################################################
# Flask Routes
#################################################

# creating 'homepage' menu options
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
# first menu option-- showing precipitation information for the most current 12 months
@app.route('/api/v1.0/precipitation')
def precipitation():   
    results = session.query(MS.date, MS.prcp).filter(MS.date>='2016-08-23').all()
    return jsonify({d:p for d,p in results})
    session.close()

# second menu option-- showing each station
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(MS.station).all()
    stations = {s for s, in results}
    return jsonify(list(stations))
    session.close()

# third menu option-- shows the most active station's temperature recordings
# from the current 12 months
@app.route('/api/v1.0/tobs')
def tobs():
    station = 'USC00519281'
    sel = [MS.station, MS.tobs, MS.date]
    active_station = session.query(*sel).filter(MS.date > '2016-08-22').filter((MS.station) == station).all()
    active = [{'station': a, 'tobs': b, 'date': c} for a, b, c in active_station]
    return jsonify(active)
    session.close()

# fourth menu option-- shows the average, minimum, and maximum temps since the date inputed
@app.route('/api/v1.0/<start>')
def start(start):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    temps = session.query(func.avg(MS.tobs),
                          func.min(MS.tobs),
                          func.max(MS.tobs)).\
                filter(MS.date >= start_date).all()
    if temps:
        min_temp, avg_temp, max_temp = temps[0]
    return {
            'min': min_temp,
            'avg': avg_temp,
            'max': max_temp
        }
    session.close()

# fifth menu option-- shows the average, minimum, and maximum temps
# to occur between the two dates inputed
@app.route('/api/v1.0/<start>/<end>')
def get_temp_stats_start_end(start, end):
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    temps = session.query(func.min(MS.tobs),
                          func.avg(MS.tobs),
                          func.max(MS.tobs)).\
                filter(MS.date >= start_date, MS.date <= end_date).all()
    if temps:
        min_temp, avg_temp, max_temp = temps[0]
        return {
            'min': min_temp,
            'avg': avg_temp,
            'max': max_temp
        }
    else:
        return {
            'error': 'no data for you'
        }
    session.close()

