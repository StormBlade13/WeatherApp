import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import json
from datetime import datetime

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..", "db")
DB_DIR = os.path.abspath(DB_DIR)

DB_PATH = os.path.join(DB_DIR, "database.db")
print(DB_PATH)

KEEP = {"TMAX", "TMIN", "PRCP"}

#Database base class
Base = declarative_base()

#Creates sqlite engine
engine = sa.create_engine(f"sqlite:///{DB_PATH}")

#Makes a session
Session = sessionmaker(bind = engine)

#station table
class StationTable(Base):

    #Table name
    __tablename__ = "Station"

    #Columns
    stationID = sa.Column(sa.String, unique = True, primary_key = True)
    stationName = sa.Column(sa.String)

#Weather records table
class WeatherTable(Base):

    __tablename__ = "Weather Records"

    #Columns
    stationID = sa.Column(sa.String, sa.ForeignKey("Station.stationID"))
    date = sa.Column(sa.Date)
    tmax = sa.Column(sa.Double)
    tmin = sa.Column(sa.Double)
    prcp = sa.Column(sa.Double)

    __table_args__ = (
        sa.PrimaryKeyConstraint("stationID", "date"),
    )

    station = relationship("StationTable")

Base.metadata.create_all(engine)

#Read raw data into memory
def readFilter() -> list:

    with open("data_raw//raw_data.json", "r") as f:
        data = json.load(f)

    data = data["results"]
    return data

#Converts 1/10th celsius into fehrenheit
def nceiTempToF(data):
    celsius = data / 10
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

#Collapses original format into a single row per date
def collapseAllData(data):
    grouped = {}

    #Iterate through each item
    for item in data:
        date = item["date"]
        dtype = item["datatype"]
        value = item["value"]

        #Only stores selected data types
        if dtype not in KEEP:
            continue

        #Creates new row if date is not already used
        if date not in grouped:
            grouped[date] = {
                "stationID": "GHCND:USW00003947",
                "date": datetime.fromisoformat(date).date(),
                "tmax": None,
                "tmin": None,
                "prcp": None
            }

        #Assigns data to coresponding dictionary key
        if dtype == "TMAX":
            grouped[date]["tmax"] = nceiTempToF(value)
        elif dtype == "TMIN":
            grouped[date]["tmin"] = nceiTempToF(value)
        elif dtype == "PRCP":
            grouped[date]["prcp"] = value

    #Returns dictionary values as a list
    return list(grouped.values())

#Inserts data into database
def insert(data):

    session = Session()
    records = collapseAllData(data)
    session.bulk_insert_mappings(WeatherTable, records)
    session.commit()


