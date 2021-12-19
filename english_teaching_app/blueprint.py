#!/usr/bin/env python3
from flask import Blueprint
sebastian_blueprint = Blueprint('sebastian',__name__)

@sebastian_blueprint.route('/<string:name>')
def home(name):
    return f"You shall prevail, {name}!"
