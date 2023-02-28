from flask import Flask

from buddywise.modules.bootstrap_database import connect_to_mongo
from buddywise.routes.companies import company_urls
from buddywise.routes.employees import employee_urls
from buddywise.routes.index import base_urls


def _create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("settings.py")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    return app


def _register_blueprints(app):
    """
    all valid blue prints need to be registered here.
    """
    app.register_blueprint(base_urls)
    app.register_blueprint(company_urls)
    app.register_blueprint(employee_urls)


def init_app(test_config=None) -> Flask:
    """
    bootstraps a flask application.
    makes connection to the database.
    """
    app = _create_app(test_config)
    _register_blueprints(app)
    # init_database_connection(app)

    return app


def run(debug: bool = False):
    """
    function to allow running thorough main.py with mongo running on docker.
    Allows for faster development
    """

    app = init_app()
    app.run(debug=debug)


def init_database_connection(app):
    """
    initialize connection to mongodb, database assignment.
    The password would have to be protected as an app / docker secret.
    """
    db_user_name = app.config["DB_USER_NAME"]
    db_password = app.config["DB_PASSWORD"]
    db_url = app.config["DB_URL"]
    host = app.config["HOST"]
    connect_to_mongo(db_user_name, db_password, db_url, host=host)


def init_app(test_config=None) -> Flask:
    """
    bootstraps a flask application.
    makes connection to the database.
    """
    app = _create_app(test_config)
    _register_blueprints(app)
    init_database_connection(app)

    return app


def run(debug: bool = False):
    """
    function to allow running thorough main.py with mongo running on docker.

    Allows for faster development
    """

    app = init_app()
    app.run(debug=debug)
