from flask import Flask, render_template, jsonify
from openSky_Lib import OpenSkyApi
import sqlite3
import configparser
import json


# Read API credentials from the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

opensky_username = config.get('opensky', 'username')
opensky_password = config.get('opensky', 'password')

app = Flask(__name__)

def create_table_if_not_exists():
    conn = sqlite3.connect('opensky_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY,
            icao24 TEXT NOT NULL,
            callsign TEXT,
            origin_country TEXT,
            time_position INTEGER,
            last_contact INTEGER,
            longitude REAL,
            latitude REAL,
            altitude REAL,
            on_ground INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def insert_states_into_db(states):
    with sqlite3.connect('opensky_data.db') as conn:
        cursor = conn.cursor()
        for state in states:
            cursor.execute('''
                INSERT INTO states (icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, altitude, on_ground)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                state.icao24,
                state.callsign,
                state.origin_country,
                state.time_position,
                state.last_contact,
                state.longitude,
                state.latitude,
                state.geo_altitude,
                state.on_ground
            ))
        conn.commit()

def get_states_from_db():
    with sqlite3.connect('opensky_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM states")
        states = cursor.fetchall()
    return states



@app.route("/")
def display_states():
    try:
        create_table_if_not_exists()
        db_states = get_states_from_db()

        # Check if there's existing data in the database
        if db_states:
            # Convert the data to a list of dictionaries
            list_of_dicts = [
                dict(
                    icao24=row[1],
                    callsign=row[2],
                    origin_country=row[3],
                    time_position=row[4],
                    last_contact=row[5],
                    longitude=row[6],
                    latitude=row[7],
                    altitude=row[8],
                    on_ground=row[9]
                )
                for row in db_states
            ]

            return render_template('index.html', states=list_of_dicts)
        else:
            return "No data available in the database. Consider fetching from the OpenSky API."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)