from flask import Flask
import os

app = Flask(__name__)
VERSION = os.environ.get("APP_VERSION", "1.0")


@app.route("/")
def index():
    return f"Jenkins + Docker CI/CD Demo\nVersion: {VERSION}\n"


@app.route("/health")
def health():
    return "OK\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
