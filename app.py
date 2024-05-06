

from flask import Flask, render_template, jsonify, request

import database
from routes.user_auth import user_auth, verify_id_token
from crypto import handler
from utils.env_handler import get_base_url, get_app_secret_key

received_data = {}
base_url = get_base_url()

app = Flask(__name__)
app.secret_key = get_app_secret_key()
app.register_blueprint(user_auth, url_prefix='/auth')


@app.route("/")
def index():
    cryptography_types = database.load_cryptography_types()
    return render_template("home.html", 
                           cryptography_types=cryptography_types, 
                           base_url=base_url)


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
@verify_id_token
def show_encryption_types():
    return jsonify(database.load_cryptography_types())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
