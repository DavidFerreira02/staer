from flask import Flask, render_template, jsonify
from OpenSkyAPI import OpenSkyApi
import sqlite3
import configparser
import json


# Read API credentials from the configuration file
config = configparser.ConfigParser()
config.read('login.ini')

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
            on_ground INTEGER,
            true_track REAL
        )
    ''')
    conn.commit()
    conn.close()

""" # Connect to the SQLite database
conn = sqlite3.connect('opensky_data.db')
cursor = conn.cursor()

# Access OpenSky API
api = OpenSkyApi('1201370', 'staer')
states = api.get_states()
for state in states.states:
    cursor.execute('''
        INSERT INTO states (icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, altitude, on_ground, true_track)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        state.icao24,
        state.callsign,
        state.origin_country,
        state.time_position,
        state.last_contact,
        state.longitude,
        state.latitude,
        state.geo_altitude,
        state.on_ground,
        state.true_track
    ))
conn.commit()
conn.close() """

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
                    on_ground=row[9],
                    true_track=row[10]
                )
                for row in db_states
            ]

            return render_template('map.html', states=list_of_dicts)
        else:
            return "No data available in the database. Consider fetching from the OpenSky API."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)