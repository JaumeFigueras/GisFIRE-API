from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from .auth import auth
import json

db = SQLAlchemy()


def create_app(db_connection=None):
    app = Flask(__name__, instance_relative_config=True)
    if db_connection is None:  # pragma: no cover
        # This settings are for real application with WSGI and Apache, so can't be tested in a testing environment
        host = request.environ.get('GISFIRE_DB_HOST'),
        port = request.environ.get('GISFIRE_DB_PORT'),
        database = request.environ.get('GISFIRE_DB_DATABASE'),
        username = request.environ.get('GISFIRE_DB_USERNAME'),
        password = request.environ.get('GISFIRE_DB_PASSWORD')
        uri = f"postgresql+psycopg2://{username}:{password}@{host}/{database}:{port}"
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
    else:
        uri = "postgresql+psycopg2://"
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {'creator': lambda: db_connection}
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.errorhandler(401)
    def page_error_401(error):
        from .user import UserAccess

        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 401)
        return jsonify(status_code=401), 401

    @app.errorhandler(404)
    def page_error_404(error):
        from .user import UserAccess

        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 404)
        return jsonify(status_code=404), 404

    @app.errorhandler(405)
    def page_error_405(error):
        from .user import UserAccess

        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 405)
        return jsonify(status_code=405), 405

    @app.route('/')
    def main():
        from .user import UserAccess

        UserAccess(request.remote_addr, request.url, request.method, json.dumps(dict(request.values)),
                   auth.current_user()).record_access(db, 500)
        return jsonify(status_code=500), 500

    from .user import user
    from .meteocat import lightning

    app.register_blueprint(user.bp)
    app.register_blueprint(lightning.bp)

    return app
