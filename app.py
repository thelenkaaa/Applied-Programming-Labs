from flask import Flask


app = Flask(__name__)


@app.route("/api/v1/hello-world-14")
def none():
    return "Hello, world 14!"


@app.route("/")
def home():
    return "Follow the link <localhost>:<port>/api/v1/hello-world-14"


if __name__ == "__main__":
    app.run()