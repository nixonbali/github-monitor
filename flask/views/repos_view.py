from grest import GRest
from flask_classful import route
from flask import jsonify
import sys
sys.path.append('../')
from models.neo4j_models import User, Repo



class ReposView(GRest):
    """
    Repo's View (/v1/repos)
    A call to /v1/repos/<repo-id> will return Repo Node with id repo-id
    """
    __model__ = {"primary": Repo}
    __selection_field__ = {"primary": "repo_id",
                            "alt": "name",
                            "secondary": {
                                "users": "login"
                            }}

    @route("/<repo_id>/users", methods=["GET"])
    def listusers(self, repo_id):
        """
        Repo's Users

        Returns a list of all User Nodes connected to Repo Node with id repo-id
        """
        try:
            repo = Repo.nodes.get(**{self.__selection_field__.get("primary"): repo_id})
            if (repo):
                users = [user.to_dict() for user in repo.users.all()]
                if (users):
                    if type(users) == type([]):
                        return jsonify({'users':users})
                    else:
                        return jsonify(users=users.to_dict), 200
                else:
                    return jsonify(errors=["Repo has no users!"]), 404
            else:
                return jsonify(errors=["Selected repo does not exists!"]), 404
        except Exception as e:
                return jsonify(errors=["An error occurred while processing your request."]), 500
