from flask import Flask, redirect, jsonify, url_for, session, render_template, request,  Response
from flask_mail import Mail, Message
import json
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import requests
from dataclasses import dataclass
from functools import wraps
import tokenizer
import secret

# User endpoints simply require a token to be supplied at the end of urls as such /<token>.
# All admin endpoints are preceeded by the word admin and they all require a request body as specified in docs


# run venv using 'pipenv shell'. The exit by just typing 'exit'.
db = SQLAlchemy()
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "45732906"
app.config["SESSION_COOKIE_NAME"] = "Waitlist"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lawaien14@gmail.com'
app.config['MAIL_PASSWORD'] = secret.emailpass
app.config['MAIL_DEFAULT_SENDER'] = 'lawaien14@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


db.init_app(app)


@dataclass
class Waitlist(db.Model):
    __tablename__ = "waitlist"
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String)
    email: str = db.Column(db.String, unique=True)
    timestamp: str = db.Column(db.String)

    def __init__(self, name, email, timestamp):
        self.name = name
        self.email = email
        self.timestamp = timestamp


with app.app_context():
    db.create_all()


def send_email(to, subject, template):
    msg = Message(subject, recipients=[to])
    msg.html = template
    mail.send(msg)

# Decorator function used to validate an admin key before allowing the user to continue with admin designated endpoint


def admin_authorizer(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        adminkey = request.json['adminkey']
        if not adminkey:
            return jsonify({"msg": "No admin key was supplied", "status": 403})
        if adminkey != secret.ADMIN_KEY:
            return jsonify({"msg": "Admin key was denied", "status": 403})

        return f(*args, **kwargs)
    return decorated


@app.route('/testing/<email>')
def test(email):
    template = f"Testingbody.<br><br>Thanks<br>The Restaurant Team"
    send_email(email, "Testing", template)
    return "email sent"


@app.route("/leavequeue/<token>", methods=['DELETE'])
def leavequeue(token):
    current_user, err = secret.decodeToken(token)
    email = current_user['useremail']
    name = current_user['name']

    if err is True:
        return "invalid token"
    try:
        user = Waitlist.query.filter_by(email=email).first()
        db.session.delete(user)
        db.session.commit()
        db.session.close()

        template = f"{name}, you have been removed from the waitlist."
        send_email(email, "You have been removed from the waitlist", template)

        response = {
            "msg": f"{name} has been removed from the waitlist", "status": 202}
        return jsonify(response)

    except:
        response = {
            "msg": f"{name} has already been removed from the waitlist", "status": 202}
        return jsonify(response)


@app.route("/admingetwaitlist", methods=['GET'])
@admin_authorizer
def admingetwaitlist():
    waitlist = Waitlist.query.order_by(Waitlist.timestamp).all()
    response = {"current_user": "admin", "waitlist": waitlist}
    return jsonify(response)


@app.route("/getwaitlist/<token>", methods=['GET'])
def getwaitlist(token):
    current_user, err = secret.decodeToken(token)
    email = current_user['useremail']
    if err is True:
        return "invalid token"
    else:
        try:
            user = Waitlist.query.filter_by(email=email).first()
            # try won't fail unless you print user.id for some reason.
            print(user.id)
            waitlist = Waitlist.query.order_by(Waitlist.timestamp).all()
            response = {"current_user": current_user, "waitlist": waitlist}
            return jsonify(response)
        except:
            response = {"msg": "User is no longer in the queue", "status": 404}
            return jsonify(response)


@app.route("/adminjoinwaitlist", methods=['POST'])
@admin_authorizer
def adminjoinwaitlist():
    # request_data = request.get_json()
    name = request.json['name']
    email = request.json['email']
    adminkey = request.json['adminkey']

    if adminkey != secret.ADMIN_KEY:
        response = {"msg": "access denied", "status": 404}
        return jsonify(response)

    session["user_email"] = email

    try:
        now = datetime.now()
        customer = Waitlist(name, email, str(now))

        # if this fails, we know that the user either already exists or something went wrong with the database
        db.session.add(customer)
        db.session.commit()
        addeduser = Waitlist.query.filter_by(email=email).first()
        client_token = secret.getToken(str(addeduser.id), name, email)
        client_url = url_for('getwaitlist', token=client_token)
        url = '127.0.0.1:5000'+str(client_url)
        token = {"msg": f"{name} was added to the waitlist",
                 "client_token": client_token, "status": 200}
        template = f"{name}, you have been added to the waitlist.<br><br>Please use this url to see your place in the queue:<br>{url}"
        send_email(email, "You have been added to the waitlist", template)
        return jsonify(token)
    except:
        try:
            db.session.rollback()
            # this tries to see if the user is already in the queue (database)
            addeduser = Waitlist.query.filter_by(email=email).first()
            client_token = secret.getToken(
                str(addeduser.id), str(addeduser.name), email)
            client_url = url_for('getwaitlist', token=client_token)
            url = '127.0.0.1:5000'+str(client_url)
            response = {"msg": "user is already in the waitlist",
                        "client_token": client_token, "status": 202}
            template = f"{name}, you have already been added to the waitlist.<br><br>Please use this url to see your place in the queue:<br>{url}"
            send_email(email, "Your waitlist link", template)
            return jsonify(response)
        except:
            # if the first two failed, something went wrong with the database
            db.session.rollback()
            response = {"msg": "something went wrong", "status": 404}
            return jsonify(response)


if __name__ == "__main__":
    app.run()
