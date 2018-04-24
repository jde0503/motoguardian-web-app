# ----------------------------------------------------------------------------
# filename: MG_DatabaseInterface.py
# description: Contains functins to interface with motoguardian database.
#
# author: Team MotoGuardian
# ----------------------------------------------------------------------------


# ---- Import necessary packages and modules ----
import psycopg2
import os


# ---- Import non-custom packages and modules ----
from motoguardianWebApp import app, connect_str


# --- Declare and initialize global variables ---
conn = None


# ---- DB SETUP ----
# Connect to the DB1
def connect_db():
    global conn
    conn = psycopg2.connect(connect_str, sslmode='require')  # sslmode='require'
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
    if (conn is not None and conn.closed == 0):
        conn.close()
