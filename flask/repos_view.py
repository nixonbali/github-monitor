from grest import GRest
from models import User, Repo
from flask_classful import route
from flask import jsonify



class ReposView(GRest):
    """Repo's View (/repos)"""
    __model__ = {"primary": Repo}
    __selection_field__ = {"primary": "id",
                            "secondary": {
                                "users": "login"
                            }}
