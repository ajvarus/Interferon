from flask import Blueprint, request, render_template, jsonify, make_response
import firebase_admin
from firebase_admin import credentials, auth, exceptions
from utils.env_handler import get_firebase_key_path, get_firebase_web_api_key
import requests
import json

user_auth = Blueprint("user_auth", __name__)

try:
    cred = credentials.Certificate(get_firebase_key_path())
    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Error: {str(e)}")

    
@user_auth.route('/signup', methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    
    elif request.method == "POST":
        data = request.json
        email = data["email"]
        password = data["password"]


        try:
            user = auth.create_user(email=email, password=password)
            return jsonify({"message": "User created successfully"}), 200
        
        except Exception as e:
            return jsonify({"message": "Failed to create user"}), 500


@user_auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        data = request.json
        email = data["email"]
        password = data["password"]
        print(email, password)

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
            print(user.json())
            user_data = user.json()
            # Create an HTTP only cookie for the idToken
            response = make_response(jsonify({'message': 'Authentication successful'}), 200)
            response.set_cookie('idToken', 
                                user_data["idToken"], 
                                httponly=True)
            return response
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Authentication failed'}), 401
             

@user_auth.route("/logout", methods=["POST"])
def logout():
    # Create a response with a message indicating successful logout
    print("Logging out")
    response = make_response(jsonify({'message': 'Logout successful'}), 200)

    # Clear the idToken cookie by setting its value to an empty string
    response.set_cookie('idToken', '', expires=0)

    return response