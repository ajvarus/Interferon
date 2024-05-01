from flask import Blueprint, request, render_template, jsonify
import firebase_admin
from firebase_admin import credentials, auth
from utils.env_handler import get_firebase_key_path

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
        print(email, password)

        try:
            user = auth.create_user(email=email, password=password)
            return jsonify({"message": "User created successfully"}), 200
        
        except Exception as e:
            return jsonify({"message": "Failed to create user"}), 500
