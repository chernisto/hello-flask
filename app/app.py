import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        message="Hello from the Raspberry Pi",
        version=os.environ.get("APP_VERSION", "dev"),
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")
