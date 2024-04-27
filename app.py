
from flask import Flask, render_template, jsonify
from database import load_encryption_types

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/api/encryption_types")
def show_encryption_types():
    return jsonify(load_encryption_types())


if __name__ == "__main__":
    app.run(debug=True, port=3000)
