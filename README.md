# WeatherApp
This project is going to collect weather data from a public API, clean it, and store it.

## Project Structure
- WeatherApp/
    - data_raw/
    - data_clean/
    - db/
    - models/
    - etl/
        - extract.py
        - transform.py
        - load.py
    - pipeline.py
    - config.py
    - requirments.txt

## Schema Design
Weather stations and daily observations.

### Tables
- Station: id, name, latitude, longitude
- WeatherRecord: id, station-id, date, temp_high, temo_low, precipitation

### Relationships
- One station -> many weather records
- WeatherRecord.station_id is a foreign key

## Extract
Download raw data into memory.
- NOAA daily summaries (JSON)

### Logic
1. Load local JSON file
2. Save raw file into data_raw/
3. Return a Pandas DataFrame for transformation

## Transform
Clean and normalize messy fields.

### Cleaning tasks
- Convert data strings into datetime.date
- Handle missing temperture values
- Normalize station names
- Convert precipitation to float
- Drop invalid rows

### Output
A clean DataFrame saved to data_clean/clean_weather.csv

## Load
Load cleaned data into SQLAlchemy ORM models

### Steps
1. Initialize engine (sqlite:///db/weather.db)
2. Create tables via Base.metadate.create_all(engine)
3. Insert stations first
4. Insert weather records with foreign keys
5. Commit in batches for performance

## Analytics
- Average temperature per month
- Hottest day per station
- Total precipitation per year
- Days above 90F
- Station with most missing data

## Pipelin Orchestration
pipeline.py runs:

    extract()
    transform()
    load()

Add logging, timestamps, and metadata table:
- PipelineRun: id, run_timestamps, raw_rows, clean_rows, loaded_rows

## Possible extentions
- Automation
- Dashboard
- Unit tests

