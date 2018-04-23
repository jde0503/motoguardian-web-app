# ---- Import necessary packages and modules ----
from flask import Flask, render_template, redirect, request
import psycopg2
import os
from datetime import datetime

# ---- APP SETUP ----
app = Flask(__name__)


# ---- DB SETUP ----
conn = None


# Connect to the DB
def connect_db():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn


# Wrap the helper function so we only open the DB once.
def get_db():
    global conn
    if conn is None:
        conn = connect_db()
    return conn


# Close the database when the request ends
@app.teardown_appcontext
def close_db(error):
    global conn
    if conn is not None:
        conn.close()


# ---- ROUTES ----

# --- Home ---
@app.route('/')
def home():
    return redirect('/landing')


# --- Landing ---
# GET landing
@app.route('/landing', methods=['GET'])
def getLanding():
    return render_template('landing.html')


# POST Landing
@app.route('/landing', methods=['POST'])
def postLanding():

    # Get database connection and cursor.
    db = get_db()
    c = db.cursor()

    # Create table in database if one does not already exist.
    c.execute("""CREATE TABLE IF NOT EXISTS Email (
                    id              SERIAL PRIMARY KEY,
                    submission_time TIMESTAMPZ NOT NULL,
                    email_address   TEXT UNIQUE NOT NULL
                    );""")

    c.execute("SET timezone = 'America/Los_Angeles';")

    # Get JSON data from request.
    email = request.get_json(force=True)["email"]

    # Insert email and relevant info into databse.
    c.exeucte("""INSERT INTO Email (submission_time, email_address)
                    VALUES (%s, %s);""",
              (datetime.now(), email))

    c.commit()

    c.execute("""SELECT * from Email;""")
    print(c.fetchall())

    c.close()

    return 'OK'
