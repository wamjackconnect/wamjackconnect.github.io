import secrets
import jwt
import datetime
import __main__

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from .models import Company, Developers, Experience
from . import db
from flask_mail import Mail, Message

auth = Blueprint('auth', __name__)


@auth.route("/registerdev", methods=["POST", "GET"])
def register_dev():
    if request.method == "POST":
        post = request.get_json()

        # Save all data fields from POST method:
        dev_name = post.get('name')
        dev_email = post.get('email')
        dev_password = post.get('password')
        dev_languages = post.get('selected')
        dev_text = post.get('text')
        dev_avatar = post.get('avatar')

        # default avatar
        if dev_avatar == "" or dev_avatar is None:
            dev_avatar = "https://us.123rf.com/450wm/asmati/asmati2005/asmati200500405/147126493-user-avatar" \
                         "-illustration-anonymous-sign-white-icon-with-gray-dropped-limitless-shadow-on-green-to-bl" \
                         ".jpg?ver=6 "

        dev_password = generate_password_hash(dev_password)

        # Query to confirm the email & username is unique:
        dev_email_q = Developers.query.filter_by(Email=dev_email).first()
        dev_name_q = Developers.query.filter_by(Username=dev_name).first()

        if dev_name_q is None and dev_email_q is None:
            try:
                # Add developer to table:
                dev = Developers(Username=dev_name, Email=dev_email, Password=dev_password, UserAvatar=dev_avatar,
                                 Status='Available', Experience=dev_text)
                db.session.add(dev)
                db.session.commit()

                # Add developer's languages to table:
                dev_id = Developers.query.filter_by(Username=dev_name).scalar()
                print(dev_languages)
                for row in dev_languages:
                    lang = Experience(DevID=dev_id.DevID, Language=row["name"])
                    db.session.add(lang)
                    db.session.commit()

                response = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }
                return jsonify(response, 200)
            except:
                response = {
                    'status': 'fail',
                    'message': 'Database error.'
                }
                return jsonify(response, 400)
        elif dev_name_q is not None:
            response = {
                'status': 'fail',
                'message': 'Name already exists.'
            }
            return jsonify(response, 403)
        elif dev_email_q is not None:
            response = {
                'status': 'fail',
                'message': 'Email already exists.'
            }
            return jsonify(response, 403)


@auth.route("/registercom", methods=["POST", "GET"])
def register_com():
    if request.method == "POST":
        post = request.get_json()

        # Save all data fields from POST method:
        com_name = post.get('name')
        com_email = post.get('email')
        com_password = post.get('password')
        com_selected = post.get('selected')
        com_bio = post.get('text')
        com_avatar = post.get('avatar')

        com_password = generate_password_hash(com_password)

        # Query to confirm the email & username is unique:
        com_email_q = Company.query.filter_by(Email=com_email).first()
        com_name_q = Company.query.filter_by(CompanyName=com_name).first()

        if com_name_q is None and com_email_q is None:
            try:
                # Add company to table:
                com = Company(CompanyName=com_name, Password=com_password, Email=com_email, Logo=com_avatar,
                              GeneralIndustry=com_selected["name"], Bio=com_bio)
                db.session.add(com)
                db.session.commit()

                response = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }
                return jsonify(response, 200)
            except:
                response = {
                    'status': 'fail',
                    'message': 'Unknown error.'
                }
                return jsonify(response, 400)
        elif com_name_q is not None:
            response = {
                'status': 'fail',
                'message': 'Name already exists.'
            }
            return jsonify(response, 403)
        elif com_email_q is not None:
            response = {
                'status': 'fail',
                'message': 'Email already exists.'
            }
            return jsonify(response, 403)


@auth.route("/developerlogin", methods=['POST', 'GET'])
def login_dev():
    if request.method == "POST":
        post = request.get_json()

        # Get login fields:
        dev_email = post.get('email')
        dev_password = post.get('password')

        # Search for developer:
        dev = Developers.query.filter_by(Email=dev_email).first()

        if dev is None:
            response = {
                'status': 'fail',
                'message': 'User does not exist'
            }
            return jsonify(response, 404)

        elif not check_password_hash(dev.Password, dev_password):
            response = {
                'status': 'fail',
                'message': 'Incorrect password'
            }
            return jsonify(response, 403)
        else:
            # Logged in and create token:
            token = jwt.encode({'user_key': dev.DevID,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                               __main__.app.config['SECRET_KEY'])
            response = {
                'status': 'success',
                'message': 'Successfully logged on.',
                'token': token
            }

            return jsonify(response, 200)


@auth.route("/companylogin", methods=['POST', 'GET'])
def login_com():
    if request.method == "POST":
        post = request.get_json()

        # Get login fields:
        com_email = post.get('email')
        com_password = post.get('password')

        # Search for company:
        com = Company.query.filter_by(Email=com_email).first()

        if com is None:
            response = {
                'status': 'fail',
                'message': 'User does not exist'
            }
            return jsonify(response, 404)

        elif not check_password_hash(com.Password, com_password):
            response = {
                'status': 'fail',
                'message': 'Incorrect password'
            }
            return jsonify(response, 403)

        else:
            # Logged in and create token:
            token = jwt.encode({'user_key': com.CompID,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                               __main__.app.config['SECRET_KEY'])
            response = {
                'status': 'success',
                'message': 'Successfully logged on.',
                'token': token
            }

            return jsonify(response, 200)


@auth.route("/forgotpasswordCom", methods=['POST', 'GET', 'PUT'])
def forgot_pass_com():
    secret_hash = secrets.token_hex(nbytes=16)
    if request.method == "POST":
        post = request.get_json()

        com_email = post.get('email')

        comp = Company.query.filter_by(Email=com_email).first()
        if comp is None:
            response = {
                'Status': 'Unsuccessful',
                'message': 'Email not found'
            }
            return jsonify(response, 403)
        else:
            mail = Mail()
            mail.init_app(__main__.app)
            msg = Message(recipients=[com_email],
                            body=secret_hash,
                            sender=__main__.app.config['MAIL_SENDER'])
            mail.send(msg)
        return jsonify(secret_hash, 200)
    elif request.method == 'PUT':
        post = request.get_json()

        email = post.get('email')
        new_password = generate_password_hash(post.get('newPass'))
        company = Company.query.filter_by(Email=email).one()
        company.Password = new_password
        db.session.commit()
        return jsonify(200)


@auth.route("/forgotpasswordDev", methods=['POST', 'GET', 'PUT'])
def forgot_pass_dev():
    if request.method == 'POST':
        secret_hash = secrets.token_hex(nbytes=16)
        post = request.get_json()
        dev_email = post.get('email')
        dev = Developers.query.filter_by(Email=dev_email).first()
        if dev is None:
            response = {
                'Status': 'Unsuccessful',
                'message': 'Email not found'
            }
            return jsonify(response, 403)
        else:
            mail = Mail()
            mail.init_app(__main__.app)
            msg = Message(secret_hash,
                          recipients=[dev_email],
                          sender=__main__.app.config['MAIL_SENDER'])
            mail.send(msg)
        return jsonify(secret_hash, 200)
    elif request.method == 'PUT':
        post = request.get_json()

        email = post.get('email')
        new_password = generate_password_hash(post.get('newPass'))
        dev = Developers.query.filter_by(Email=email).one()
        dev.Password = new_password
        db.session.commit()
        return jsonify(200)

def decode_token(token):
    if not token:
        return -1
    try:
        data = jwt.decode(token, __main__.app.config['SECRET_KEY'], algorithms='HS256')
    except:
        return -1  # invalid token
    return data['user_key']
