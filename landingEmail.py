# ---- Import necessary packages and modules ----
from flask_mail import Mail, Message
from motoguardianWebApp import app

# --- Declare and initialize global variables ---
MAIL_DEFAULT_SENDER = ("MotoGuardian", "motoguardian140@gmail.com")


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
    sendEmail(
        recipients=[recipient],
        subject="MotoGuardian - Thank You!",
        body="Thank you for signing up to receive updates about our product."
    )
