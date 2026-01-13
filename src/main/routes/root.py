from flask import Blueprint, redirect


root_route = Blueprint('/', __name__)


@root_route.route('/')
def index():
    return redirect('/catalogo')
