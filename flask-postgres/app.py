from flask import Flask #, jsonify
from secrets import POSTGRES
from pr_model import PRModel, PRSchema, rdb, ma


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
rdb.init_app(app)
ma.init_app(app)

pr_schema = PRSchema()
prs_schema = PRSchema(many=True)


@app.route('/')
def main():
    return 'Hello World!'

@app.route('/pullrequest/examples')
def example_pull_requests():
    prs = PRModel.all_prs()
    return {"pullrequests": prs_schema.dump(prs[:3])}


@app.route('/pullrequest/id/<id>')
def single_pull_request(id):
    prs = PRModel.get_pr_by_id(id)
    return {"pullrequests": prs_schema.dump(prs)}

# test id: 645165

@app.route('/pullrequest/repo/<user>/<repo>')
def repo_pull_requests(user, repo):
    prs = PRModel.get_pr_by_repo("/".join((user,repo)))
    return {"pullrequests": prs_schema.dump(prs)}

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(host="localhost", port=5000)
