from flask import Blueprint

base_urls = Blueprint("index", __name__)


@base_urls.route("/", methods=["GET"])
def index():
    return "<h1>Hello from Flask & Docker</h2>"
