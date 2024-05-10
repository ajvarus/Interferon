

from flask import Flask, render_template, jsonify, request, session

import database as db
import celerify
from routes.user_auth import user_auth, verify_id_token
from crypto import handler 
from utils.env_handler import get_base_url, get_app_secret_key, get_celery_broker_url, get_celery_result_backend


received_data = {}

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL=get_celery_broker_url(),
    CELERY_RESULT_BACKEND=get_celery_result_backend()
)
app.secret_key = get_app_secret_key()
app.register_blueprint(user_auth, url_prefix='/auth')

# Create a Celery app
celery = celerify.make_celery(app)


@app.route("/")
def index():
    return render_template("index.html",
                           base_url= get_base_url(request.host))

@app.route("/dashboard", methods = ["GET", "POST"])
@verify_id_token
def show_dashboard():
        if request.method == "GET":
            return render_template("dashboard.html",
                                username = session.get("username"),
                                base_url = get_base_url(request.host))
        
        if request.method == "POST":
            return jsonify({
                "message": "Logout successful"
            })


@app.route("/cryptography/<crypt_name>", methods = ["GET", "POST"])
def show_crypt_page(crypt_name):
    if request.method == "GET":
        try:
            crypt_types = db.load_cryptography_types()
            crypt_type = next((row 
                               for row in crypt_types 
                               if row["display_name"].lower() == crypt_name), 
                               None)
            
            crypt_type_enums = db.load_crypt_type_enums(crypt_type["id"])

            return render_template("cryptography.html", 
                                crypt_type = crypt_type, 
                                crypt_type_enum = crypt_type_enums,
                                base_url=get_base_url(request.host))
        except Exception as e:
            return jsonify({
                "message": f"Invalid request {str(e)}"
            })
    
    elif request.method == "POST":
        data = request.json
        text = data['plaintext']
        enum_id = int(data['cryptEnumType'])
        # Placeholder for actual encryption logic
        ciphertext = handler.crypto_handler(enum_id, text)
        return jsonify(ciphertext=ciphertext)

# Endpoints for setting internal variables
@app.route("/internal/crypt_type_id", methods = ["POST"])
@verify_id_token
def receive_crypt_id():
    data = request.get_json()
    crypt_id = data.get("info")
    received_data["crypt_id"] = crypt_id
    return jsonify(data)

# Endpoints for third-party services
@app.route("/api/encryption_types")
@verify_id_token
def show_encryption_types():
    return jsonify(db.load_cryptography_types())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3000)
