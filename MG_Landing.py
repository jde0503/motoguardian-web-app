# ----------------------------------------------------------------------------
# filename: MG_Landing.py
# description: Contains functins used on motoguardian landing page.
#
# author: Team MotoGuardian
# ----------------------------------------------------------------------------


# ---- Import necessary packages and modules ----
from flask_mail import Mail, Message
from datetime import datetime


# ---- Import custom packages and modules ----
from motoguardianWebApp import app
from MG_DatabaseInterface import get_db


# --- Declare and initialize global variables ---
verbose = False
MAIL_DEFAULT_SENDER = ("MotoGuardian", "motoguardian140@gmail.com")


# Returns true if email is valid and unique. Returns false otherwise.
def validateEmail(email_address):
    # Get database connection and cursor.
    db = get_db()
    c = db.cursor()

    # Query database for entries with provided email address.
    c.execute("""SELECT COUNT(Email)
                 FROM Email
                 WHERE email_address=%s;""",
              (email_address,))
    count = int(c.fetchone()[0])
    c.close()

    if (verbose):
        print("Count: " + str(count))

    if (count == 0 and len(email_address) > 6):
        return True
    else:
        return False


# Inserts email address into database.
def insertEmail(email_address):
    # Get database connection and cursor.
    db = get_db()
    c = db.cursor()

    # Insert email and relevant info into databse.
    c.execute("""INSERT INTO Email (submission_time, email_address)
                    VALUES (%s, %s);""",
              (datetime.now(), email_address))
    db.commit()

    if (verbose):
        c.execute("""SELECT * from Email;""")
        print(c.fetchall())

    c.close()


# General function to send email.
def sendEmail(recipients, subject, body):

    app.config.from_pyfile('email_config.cfg')
    mail = Mail(app)

    msg = Message(
        sender=MAIL_DEFAULT_SENDER,
        recipients=recipients,
        subject=subject,
        body=body)

    with app.app_context():
        mail.send(msg)


# Wrapper for use with landing page.
def sendThanks(recipient):
    with open('email_body.txt', 'r') as file:
        sendEmail(
            recipients=[recipient],
            subject="MotoGuardian - Thank You!",
            body=file.read()
        )
