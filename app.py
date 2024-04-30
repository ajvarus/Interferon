
import firebase_admin.exceptions
from flask import Flask, render_template, jsonify, request
import database
from cryptography import handler
import firebase_admin
from firebase_admin import credentials, auth, exceptions
import dotenv
import os

dotenv.load_dotenv()

try:
    cred = credentials.Certificate(os.getenv("FIREBASE_KEY_PATH"))
    firebase_app = firebase_admin.initialize_app(cred)
    print(firebase_app.credential)
except Exception as e:
    print(f"Error: {str(e)}")

received_data = {}

app = Flask(__name__)

@app.route("/")
def index():
    cryptography_types = database.load_cryptography_types()
    return render_template("home.html", cryptography_types=cryptography_types)

@app.route('/signup', methods=["POST", "GET"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html")
    
    elif request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        print(email, password)

        try:
            user = auth.create_user(email=email, password=password)
            return jsonify({"message": "User created successfully"}), 200
        except exceptions.FirebaseError as e:
            return jsonify({"error": "Authentication failed", "reason": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Failed to create user", "reason": str(e)}), 500


@app.route("/cryptography/<crypto_type>", methods = ["GET", "POST"])
def show_crypt_page(crypto_type):
    if request.method == "GET":
        crypt_type = database.load_selected_crypt_type(received_data["crypt_id"])
        crypt_type_enum = database.load_crypt_type_enums(received_data["crypt_id"])
        return render_template("cryptography.html", 
                            crypt_type = crypt_type, 
                            crypt_type_enum = crypt_type_enum)
    
    elif request.method == "POST":
        data = request.json
        text = data['plaintext']
        enum_id = int(data['cryptEnumType'])
        # Placeholder for actual encryption logic
        ciphertext = handler.handler(enum_id, text)
        return jsonify(ciphertext=ciphertext)

# Endpoints for setting internal variables
@app.route("/internal/crypt_type_id", methods = ["POST"])
def receive_crypt_id():
    data = request.get_json()
    crypt_id = data.get("info")
    received_data["crypt_id"] = crypt_id
    return jsonify(data)

# Endpoints for third-party services
@app.route("/api/encryption_types")
def show_encryption_types():
    return jsonify(database.load_encryption_types())


if __name__ == "__main__":
    app.run(debug=True, port=3000)
