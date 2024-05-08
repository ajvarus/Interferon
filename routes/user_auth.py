from flask import Blueprint, request, render_template, jsonify, make_response, redirect, session, url_for
import firebase_admin
from firebase_admin import credentials, auth
import requests
import json
from functools import wraps
from base64 import b64encode
from celery import shared_task, chain

from utils.env_handler import get_firebase_key_path, get_firebase_web_api_key, get_base_url
from crypto.key_gen import generate_master_key, generate_derived_key
import database as db
import celerify as cl

user_auth = Blueprint("user_auth", __name__)

try:
    cred = credentials.Certificate(get_firebase_key_path())
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Error: {str(e)}")

    
@user_auth.route('/signup', methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html", base_url=get_base_url(request.host))
    
    elif request.method == "POST":
        data = request.json
        email = data["email"]
        password = data["password"]

        try:
            user = auth.create_user(email=email, password=password)
            response = signin_with_email_and_password(email, password)
           
            session["uid"] = user.uid

            if response.status_code == 200:
                master_key = generate_master_key(password)
                session["master_key"] = master_key

                cl.handle_user_creation.delay(user.uid, master_key)
                
                return response
                # return redirect(url_for("user_auth.signup_success"))
            else:
                raise Exception("Failed to create user")
    
        except Exception as e:
            return jsonify({"message": "Failed to create user"}), 500

@user_auth.route('/signup_success')
def signup_success():
    master_key = session.pop("master_key") # Remove master key from session after retrieval
    if master_key:
        encoded_master_key = b64encode(master_key).decode()
        uid = session.pop("uid")
        cl.handle_keygen.delay(uid, encoded_master_key)

        return render_template('signup_success.html', master_key=encoded_master_key)
    else:
        return redirect(url_for('signup'))


@user_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", base_url=get_base_url(request.host))
    
    elif request.method == "POST":
        data = request.json
        email = data["email"]
        password = data["password"]
        print(email, password)

        response = signin_with_email_and_password(email, password)

        return response
        

@user_auth.route("/logout", methods=["POST"])
def logout():
    # Create a response with a message indicating successful logout
    print("Logging out")
    response = make_response(jsonify({'message': 'Logout successful'}), 200)

    # Clear the idToken cookie by setting its value to an empty string
    response.set_cookie('idToken', '', expires=0)

    return response

# The below decorators are used for session management
def verify_id_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            id_token = request.cookies["idToken"]
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            # Extract UID from the decoded token
            uid = decoded_token['uid']
            print(uid)
            # Pass the UID to the route function
            return func(*args, **kwargs)
        except KeyError:
            return jsonify({'error': 'Authorization header missing'}), 401
        except auth.InvalidIdTokenError:
            return jsonify({'error': 'Invalid ID token'}), 401

    return wrapper

@shared_task
def signin_with_email_and_password(email, password):
    payload = json.dumps({
            "email": email,
            "password": password,
            "return_secure_token": True
        })

    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    try:
        user = requests.post(rest_api_url,
                params={"key": get_firebase_web_api_key()},
                data=payload)
        user_data = user.json()
        # Create an HTTP only cookie for the idToken
        response = make_response(jsonify({'message': 'Login successful'}), 200)
        response.set_cookie('idToken', 
                            user_data["idToken"], 
                            httponly=True)
        return response
    except Exception as e:
        return jsonify({'message': 'Login failed'}), 401