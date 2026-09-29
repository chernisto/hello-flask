import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        message="Hello from the Raspberry Pi. Just added the webhook!!",
        version=os.environ.get("APP_VERSION", "dev"),
    )


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")
