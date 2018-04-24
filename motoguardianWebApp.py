# ----------------------------------------------------------------------------
# filename: motoguardianWebApp.py
# description: Contains the routing for the motoguardian web app
#
# author: Team MotoGuardian
# ----------------------------------------------------------------------------


# ---- Import non-custom packages and modules ----
from flask import Flask, render_template, redirect, request, abort


# ---- APP SETUP ----
app = Flask(__name__)


# ---- Import custom packages and modules ----
from MG_DatabaseInterface import get_db
from MG_Landing import validateEmail, insertEmail, sendThanks


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
    db.commit()
    c.close()

    # Get JSON data from request.
    email_address = str(request.get_json(force=True)["email_address"])

    if (validateEmail(email_address)):
        insertEmail(email_address)
        sendThanks(email_address)
        return 'OK'
    else:
        abort(406)
        return "Email Invalid"
