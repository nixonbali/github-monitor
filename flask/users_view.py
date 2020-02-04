from grest import GRest
from models import User
from flask_classful import route
from flask import jsonify


class ReposView(GRest):
    __model__ = {"Primary": Repo}
    __selection_field__ {"primary": "name",
                            "secondary": {
                                "users": ""
                            }}


class UsersView(GRest):
    __model__ = {"primary": User}
    __selection_field__ = {"primary": "login",
                            "secondary": {
                                "repos": "name"
                            }}

    @route("/<login>/repos", methods=["GET"])
    def listrepos(self, login):
        print('here')
        try:
            user = User.nodes.get(**{self.__selection_field__.get("primary"): str(markupsafe.escape(login))})
            if (user):
                repos = user.repos.get()
                print("here")
                if (repos):
                    print('repos')
                    return jsonify(repos=repos.to_dict()), 200
                else:
                    return jsonify(errors=["User has no repos!"]), 404
            else:
                return jsonify(errors=["Selected user does not exists!"]), 404
    #
    #
    #
    #
    # def owner(self, pet_id):
    #     try:
    #         pet = Pet.nodes.get(**{self.__selection_field__.get("primary"):
    #                                str(markupsafe.escape(pet_id))})
    #
    #         if (pet):
    #             current_owner = pet.owner.get()
    #             if (current_owner):
    #                 return jsonify(owner=current_owner.to_dict()), 200
    #             else:
    #                 return jsonify(errors=["Selected pet has not been adopted yet!"]), 404
    #         else:
    #             return jsonify(errors=["Selected pet does not exists!"]), 404
        except:
            return jsonify(errors=["An error occurred while processing your request."]), 500
