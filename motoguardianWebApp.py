# ---- Import necessary packages and modules ----
from flask import Flask, render_template, redirect, request, abort
import psycopg2
import os
from datetime import datetime
#from landingEmail import sendThanks


# --- Declare and initialize global variables ---
verbose = True
conn = None


# ---- APP SETUP ----
app = Flask(__name__)


# ---- DB SETUP ----
# Connect to the DB
def connect_db():
    global conn
    connect_str = "dbname='testMotoguardian' user='vagrant' host='localhost'"
    conn = psycopg2.connect(connect_str)
    return conn


# Wrap the helper function so we only open the DB once
def get_db():
    global conn
    if (conn is None or conn.closed != 0):
        conn = connect_db()
    return conn


# Close the database when the request ends
@app.teardown_appcontext
def close_db(error):
    global conn
    if conn is not None:
        conn.close()


# ---- Helper Functions ----
# Returns true if email is valid and unique. Returns false otherwise.
def validateEmail(email_address):
    # Get database connection and cursor.
    db = get_db()
    c = db.cursor()

    # Query database for entries with provided email address.
    c.execute("""SELECT COUNT(Email)
                 FROM Email
                 WHERE email_address=('%s');""",
              (email_address))
    count = int(c.fetchone())
    c.close()

    if (verbose):
        print("Count" + str(count))

    if (count == 0 and len(email_address) > 6):
        return True
    else:
        return False


# Inserts email address into database.
def insertEmail(email_address):
    print(email_address)

    # Get database connection and cursor.
    db = get_db()
    c = db.cursor()

    # Insert email and relevant info into databse.
    c.execute("""INSERT INTO Email (submission_time, email_address)
                    VALUES (%s, %s);""",
              (datetime.now(), email_address))
    db.commit()
    c.close()

    if (verbose):
        c.execute("""SELECT * from Email;""")
        print(c.fetchall())


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
                    submission_time TIMESTAMP NOT NULL,
                    email_address   TEXT UNIQUE NOT NULL
                    );""")

    # Get JSON data from request.
    email_address = str(request.get_json(force=True)["email_address"])

    if (validateEmail(email_address)):
        insertEmail(email_address)
        # sendThanks(email_address)
        return 'OK'
    else:
        abort(406)
        return "Email Invalid"
