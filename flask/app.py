from flask import Flask, render_template, request, redirect, url_for, jsonify
from secrets import POSTGRES, NEO4J_HOST
from models.pr_model import PRModel, PRSchema, rdb, ma
import requests
import json
import neomodel
from grest import global_config
from views.users_view import UsersView
from views.repos_view import ReposView
from models.neo4j_models import Repo


app = Flask(__name__)

"""Connection to Postgres"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
rdb.init_app(app)
ma.init_app(app)

"""Connection to Neo4j"""
# configure connection to database
neomodel.config.DATABASE_URL = NEO4J_HOST # The bolt URL of your Neo4j instance
neomodel.config.AUTO_INSTALL_LABELS = True
neomodel.config.FORCE_TIMEZONE = True  # default False


pr_schema = PRSchema()
prs_schema = PRSchema(many=True)

@app.route('/')
def main():
    return 'Hello World!'

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/process', methods = ['POST'])
def process():
    username = request.form['username']
    repo = request.form['repo']
    ### user-only input
    if repo == '':
        collabs = requests.get("http://0.0.0.0:5000" + url_for('UsersView:listcollabs', login=username)).json()
        return jsonify(collabs)
    ### repo input
    pull_requests = requests.get("http://0.0.0.0:5000" + url_for('repo_pull_requests',user=username,repo=repo)).json()['pullrequests']
    num_pr = len(pull_requests)
    if num_pr == 0:
        return jsonify({'error': 'username / repo non-existent or contains no pull requests'})
    else:
        ### PR Metrics
        merge_rate = sum([pr['merged'] for pr in pull_requests])/num_pr
        metrics = requests.get("http://0.0.0.0:5000" + url_for('repo_metrics',user=username,repo=repo)).json()
        metrics['num_pr'] = num_pr
        metrics['merge_rate'] = merge_rate
        mean_open_time = requests.get("http://0.0.0.0:5000" + url_for('repo_pr_time',user=username,repo=repo)).json()
        metrics.update(mean_open_time)

        ### Connections
        rv = ReposView()
        repo_id = Repo.nodes.get(**{rv.__selection_field__.get("alt"): "/".join((username,repo))}).repo_id
        #print(repo_id)
        users = requests.get("http://0.0.0.0:5000" + url_for('ReposView:listusers',repo_id = repo_id)).json()
        #print(users)
        metrics.update(users)
        return jsonify(metrics)

"""

API Calls

"""
@app.route('/v1/pullrequest/examples')
def example_pull_requests():
    prs = PRModel.all_prs()
    return {"pullrequests": prs_schema.dump(prs[:3])}

"""Pull Request by PR ID"""
@app.route('/v1/pullrequest/id/<id>')
def single_pull_request(id):
    prs = PRModel.get_pr_by_id(id)
    return {"pullrequests": prs_schema.dump(prs)}
# test id: 645165

"""Pull Requests by Repo"""
@app.route('/v1/pullrequest/repo/<user>/<repo>')
def repo_pull_requests(user, repo):
    prs = PRModel.get_pr_by_repo("/".join((user,repo)))
    return json.dumps({"pullrequests": prs_schema.dump(prs)})

"""PR Metrics by Repo"""
@app.route('/v1/metrics/repo/<user>/<repo>')
def repo_metrics(user, repo):
    metrics = PRModel.get_repo_metrics("/".join((user,repo)))
    return json.dumps(pr_schema.dump(metrics))

"""PR Open Time by Repo"""
@app.route('/v1/pr_time/repo/<user>/<repo>')
def repo_pr_time(user, repo):
    pr_time = PRModel.get_repo_pr_time("/".join((user,repo)))[0]
    hours, seconds = divmod(pr_time.seconds, 3600)
    return {
        'days' : pr_time.days,
        'hours': hours,
        'minutes': seconds / 60,
      }

"""Neo4j Views"""
UsersView.register(app, route_base="/v1/users", trailing_slash=False)
ReposView.register(app, route_base="/v1/repos", trailing_slash=False)

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(host="0.0.0.0", port=5000)
