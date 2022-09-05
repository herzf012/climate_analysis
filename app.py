#################################################
# Import Dependences
#################################################
from os import stat
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect = True)

# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

 # Home page showing available paths to get JSON data from the database
@app.route("/")
def home():

    print("Server recieved request for 'Home' page...")

    return (
        f"Welcome to my climate app!<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>yyyy-mm-dd<br/>"
        f"/api/v1.0/<start>yyyy-mm-dd/<end>yyyy-mm-dd<br/>"
    )

# Returns a page with JSON data with dates as keys and precipitation values as values
@app.route("/api/v1.0/precipitation")
def precipitation():

    print("Server recieved request for 'precipitation' page...")

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_date_prcp = []

    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict[date] = prcp
        all_date_prcp.append(date_prcp_dict)

    return jsonify(all_date_prcp)

# Returns a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():

    print("Server recieved request for 'stations' page...")

    session = Session(engine)

    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Return a JSON list of temperature observations (TOBS) for the previous year for the most active weather station.
@app.route("/api/v1.0/tobs")
def tobs():

    print("Server recieved request for 'tobs' page...")

    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    last_date_tuple = tuple(map(int, last_date.split("-")))

    year_ago = dt.date(last_date_tuple[0], last_date_tuple[1], last_date_tuple[2]) - dt.timedelta(days = 365)

    year_ago = year_ago.strftime("%Y-%m-%d")

    total_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc()).all()

    most_active_station = total_stations[0][0]

    results = session.query(Measurement.tobs)\
    .filter(Measurement.station == most_active_station, Measurement.date >= year_ago).all()

    temps = list(np.ravel(results))

    return jsonify(temps)

# Returns min, max, and avg temps for all dates after and including the start date
@app.route("/api/v1.0/<start>")
def start_date(start):

    print("Server recieved request for 'start' page...")

    session = Session(engine)

    try:

        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
            .filter(Measurement.date >= start).all()

        temps = list(np.ravel(results))

        temps_dict = {}

        temps_list = []

        temps_dict["min"] = temps[0]

        temps_dict["max"] = temps[1]

        temps_dict["avg"] = temps[2]


        temps_list.append(temps_dict)

        session.close()

        return jsonify(temps_list)

    except:

        session.close()

        return(f"'{start}' not recognised. Use yyyy-mm-dd format.")

# Returns min, max, and avg temps for all dates after and including the start date and before and including the end date
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    print("Server recieved request for 'start/end' page...")

    session = Session(engine)

    try:

        results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs))\
            .filter(Measurement.date >= start, Measurement.date <= end).all()

        temps = list(np.ravel(results))

        temps_dict = {}

        temps_list = []

        temps_dict["min"] = temps[0]

        temps_dict["max"] = temps[1]

        temps_dict["avg"] = temps[2]


        temps_list.append(temps_dict)

        session.close()

        return jsonify(temps_list)

    except:

        session.close()

        return(f"'{start}' or '{end}' not recognised. Use yyyy-mm-dd format.")

if __name__ == "__main__":
    app.run(debug = True)