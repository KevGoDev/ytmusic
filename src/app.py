from flask import Flask
from flask_cors import CORS

from utils.database import db_init


def create_app():
    app = Flask(__name__, static_folder="static/")
    app.secret_key = "super secret"
    CORS(app, resources={r"/*": {"origins": "*"}})

    # init db
    db_init()

    # register routes
    from api import auth, status

    app.register_blueprint(status.bp)
    app.register_blueprint(auth.bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
