from OpenSkyAPI import OpenSkyApi
import sqlite3
import login

# Connect to the SQLite database
conn = sqlite3.connect('opensky_data.db')
cursor = conn.cursor()

# Access OpenSky API
api = OpenSkyApi(login.username, login.password)
states = api.get_states()

# Connect to the SQLite database (creates a new one if it doesn't exist)
conn = sqlite3.connect('opensky_data.db')
cursor = conn.cursor()

# Create a table to store state information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        icao24 TEXT,
        callsign TEXT,
        origin_country TEXT,
        time_position INTEGER,
        last_contact INTEGER,
        longitude REAL,
        latitude REAL,
        baro_altitude REAL,
        velocity REAL,
        true_track REAL,
        vertical_rate REAL,
        sensors TEXT,
        geo_altitude REAL,
        squawk TEXT,
        spi INTEGER,
        position_source INTEGER
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()

# Insert received data into the database
for state in states.states:
    cursor.execute('''
        INSERT INTO states 
        (icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, baro_altitude, 
        velocity, true_track, vertical_rate, sensors, geo_altitude, squawk, spi, position_source) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        state.icao24, state.callsign, state.origin_country, state.time_position, state.last_contact,
        state.longitude, state.latitude, state.baro_altitude, state.velocity, state.true_track, state.vertical_rate,
        str(state.sensors), state.geo_altitude, state.squawk, state.spi, state.position_source
    ))

# Commit changes and close connection
conn.commit()
conn.close()