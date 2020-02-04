import sys
from secrets import NEO4J_HOST

## built off of https://github.com/mostafa/grest example

import os
import logging
import neomodel
from flask import Flask
from grest import global_config
from users_view import UsersView
from repos_view import ReposView

app = Flask(__name__)

# #### Export flask app env variable before run
# $ export FLASK_APP=hello.py
# $ flask run

@app.route('/')
def hello_world():
    return 'hello, world!'

# configure connection to database
neomodel.config.DATABASE_URL = NEO4J_HOST # The bolt URL of your Neo4j instance
neomodel.config.AUTO_INSTALL_LABELS = True
neomodel.config.FORCE_TIMEZONE = True  # default False

# attach logger to flask's app logger
app.ext_logger = app.logger

# register users' view
UsersView.register(app, route_base="/users", trailing_slash=False)
ReposView.register(app, route_base="/repos", trailing_slash=False)

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
