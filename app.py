
from flask import Flask, render_template, jsonify
import database

app = Flask(__name__)


@app.route("/")
def index():
    cryptography_types = database.load_cryptography_types
    return render_template("home.html", cryptography_types)

@app.route("/api/encryption_types")
def show_encryption_types():
    return jsonify(database.load_encryption_types)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
