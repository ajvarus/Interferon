
from flask import Flask, render_template, jsonify, request
import json
import database

app = Flask(__name__)

received_data = {}

@app.route("/")
def index():
    cryptography_types = database.load_cryptography_types()
    return render_template("home.html", cryptography_types=cryptography_types)

@app.route("/cryptography")
def show_crypt_page():
    crypt_type_enum = database.load_crypt_type_enums(received_data["crypt_id"])
    print(crypt_type_enum)
    return jsonify(crypt_type_enum)

@app.route("/internal/crypt_type_id", methods = ["POST"])
def receive_crypt_id():
    data = request.get_json()
    crypt_id = data.get("info")
    received_data["crypt_id"] = crypt_id
    return jsonify(data)

@app.route("/api/encryption_types")
def show_encryption_types():
    return jsonify(database.load_encryption_types())


if __name__ == "__main__":
    app.run(debug=True, port=3000)
