from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def map_view():
    conn = sqlite3.connect('opensky_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM states')
    data = cursor.fetchall()
    conn.close()
    return render_template('map.html' ,states=data)

if __name__ == '__main__':
    app.run(debug=True)