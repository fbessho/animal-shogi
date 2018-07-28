from flask import Flask, url_for

app = Flask(__name__)


@app.route("/")
def hello():
    return app.send_static_file('index.html')


@app.route("/img/<path>")
def image(path):
    return app.send_static_file('img/' + path)
