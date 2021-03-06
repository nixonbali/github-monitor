from grest import GRest
from flask_classful import route
from flask import jsonify
import sys
sys.path.append('../')
from models.neo4j_models import User, Repo



class UsersView(GRest):
    """
    User's View (/v1/users)
    A call to /v1/users/<login> will return User Node with login <login>
    """
    __model__ = {"primary": User,
                    "secondary": {
                        "repos": Repo
                    }}
    __selection_field__ = {"primary": "login",
                            "secondary": {
                                "repos": "repo_id"
                            }}

    @route("/<login>/repos", methods=["GET"])
    def listrepos(self, login):
        """
        User's Repos

        Returns a list of all Repo Nodes connected to User Node with login <login>
        """
        try:
            user = User.nodes.get(**{self.__selection_field__.get("primary"): login})
            if (user):
                repos = [repo.to_dict() for repo in user.repos.all()]
                if (repos):
                    if type(repos) == type([]):
                        return jsonify({'repos':repos})
                    else:
                        return jsonify(repos=repos.to_dict), 200
                else:
                    return jsonify(errors=["User has no repos!"]), 404
            else:
                return jsonify(errors=["Selected user does not exists!"]), 404
        except Exception as e:
                return jsonify(errors=["An error occurred while processing your request."]), 500

    @route("<login>/collabs", methods = ["GET"])
    def listcollabs(self, login):
        """
        User's Connections

        Returns a list of all User Nodes with shared Repo Node connections
        to User Node with login <login>
        """
        try:
            user = User.nodes.get(**{self.__selection_field__.get("primary"): login})
            if (user):
                repos = user.repos.all()
                if (repos):
                    all_collabs = []
                    for repo in repos:
                        for collab in repo.users.all():
                            if collab not in all_collabs:
                                all_collabs.append(collab)
                    return jsonify({'users':[collab.to_dict() for collab in all_collabs]})
                else:
                    return jsonify(errors=["User has no repos!"]), 404
            else:
                return jsonify(errors=["Selected user does not exists!"]), 404
        except Exception as e:
                return jsonify(errors=["An error occurred while processing your request."]), 500
