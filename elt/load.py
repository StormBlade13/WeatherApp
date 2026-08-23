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
    tmax = sa.Column(sa.Integer)
    tmin = sa.Column(sa.Integer)
    prcp = sa.Column(sa.Integer)

    __table_args__ = (
        sa.PrimaryKeyConstraint("stationID", "date"),
    )

    station = relationship("StationTable")

Base.metadata.create_all(engine)

def readFilter() -> list:

    with open("data_raw//raw_data.json", "r") as f:
        data = json.load(f)

    data = data["results"]
    return data


def nceiTempToF(data):
    celsius = data / 10
    fahrenheit = celsius * 9/5 + 32
    return fahrenheit


def collapseAllData(data):
    grouped = {}


    for item in data:
        date = item["date"]
        dtype = item["datatype"]
        value = item["value"]

        if dtype not in KEEP:
            continue

        if date not in grouped:
            grouped[date] = {
                "stationID": "GHCND:USW00003947",
                "date": datetime.fromisoformat(date).date(),
                "tmax": None,
                "tmin": None,
                "prcp": None
            }

        if dtype == "TMAX":
            grouped[date]["tmax"] = nceiTempToF(value)
        elif dtype == "TMIN":
            grouped[date]["tmin"] = nceiTempToF(value)
        elif dtype == "PRCP":
            grouped[date]["prcp"] = value

    return list(grouped.values())

def insert(data):

    session = Session()
    records = collapseAllData(data)
    session.bulk_insert_mappings(WeatherTable, records)
    session.commit()

data = readFilter()
insert(data)

