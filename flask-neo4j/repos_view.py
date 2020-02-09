from grest import GRest
from neo4j_models import User, Repo
from flask_classful import route
from flask import jsonify



class ReposView(GRest):
    """Repo's View (/repos)"""
    __model__ = {"primary": Repo}
    __selection_field__ = {"primary": "repo_id",
                            "secondary": {
                                "users": "login"
                            }}

    @route("/<repo_id>/users", methods=["GET"])
    def listrepos(self, repo_id):
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
