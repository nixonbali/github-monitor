from grest import GRest
from models import User, Repo
from flask_classful import route
from flask import jsonify
#import markupsafe





class UsersView(GRest):
    """User's View (/users)"""
    __model__ = {"primary": User,
                    "secondary": {
                        "repos": Repo
                    }}
    __selection_field__ = {"primary": "login",
                            "secondary": {
                                "repos": "id"
                            }}

    @route("/<login>/repos", methods=["GET"])
    def listrepos(self, login):
        print('here')
        try:
            print('trying')
            print({self.__selection_field__.get("primary"): login})
            #print(**{self.__selection_field__.get("primary"): str(markupsafe.escape(login))})
            user = User.nodes.get(**{self.__selection_field__.get("primary"): login})
            print('switching')
            if (user):
                print()
                print(user.repos)
                repos = user.repos.get()
                print("here")
                if (repos):
                    print('repos')
                    return jsonify(repos=repos.to_dict()), 200
                else:
                    return jsonify(errors=["User has no repos!"]), 404
            else:
                return jsonify(errors=["Selected user does not exists!"]), 404

            # definition = dict(node_class=User, direction=OUTGOING,
            #                   relation_type=None, model=None)
            # relations_traversal = Traversal(user, User.__label__,
            #                                 definition)
            # all_users_relations = relations_traversal.all()
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
