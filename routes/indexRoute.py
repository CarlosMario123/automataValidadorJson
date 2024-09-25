from flask import Blueprint, render_template

indexRoute = Blueprint('indexRoute', __name__, url_prefix="/")


@indexRoute.route('/')
def index():
    return render_template("index.html")