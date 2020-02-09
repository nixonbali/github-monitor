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
        print('here')
        try:
            print('trying')
            print({self.__selection_field__.get("primary"): repo_id})
            #print(**{self.__selection_field__.get("primary"): str(markupsafe.escape(login))})
            repo = Repo.nodes.get(**{self.__selection_field__.get("primary"): repo_id})
            print('switching')
            if (repo):
                # definition = dict(node_class=Person, direction=OUTGOING, relation_type=None, model=None)
                # relations_traversal = Traversal(jim, Person.__label__, definition)
                # all_jims_relations = relations_traversal.all()
                #print(user.repos())
                users = [user.to_dict() for user in repo.users.all()]

                print("here")
                if (users):
                    print(users)
                    if type(users) == type([]):

                        print({'users':users})
                        return jsonify({'users':users})
                    else:
                        return jsonify(users=users.to_dict), 200
                else:
                    return jsonify(errors=["Repo has no users!"]), 404
            else:
                return jsonify(errors=["Selected repo does not exists!"]), 404
        except Exception as e:
                print(type(e))
                print(e)
                return jsonify(errors=["An error occurred while processing your request."]), 500
