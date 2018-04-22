from flask_mail import Mail, Message

from mail_config import *
from motoguardian_web_app import app


def send_email(recipients, subject, body):
    app.config.from_pyfile('mail_config.cfg')
    mail = Mail(app)
    
    msg = Message(
        sender=MAIL_DEFAULT_SENDER,
        recipients=recipients,
        subject=subject,
        body=body)

    with app.app_context():
        mail.send(msg)