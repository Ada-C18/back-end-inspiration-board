from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.board import Board
    from app.models.card import Card
    from app.models.user import User


    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from . import board_routes, card_routes, user_routes
    app.register_blueprint(board_routes.bp)
    app.register_blueprint(card_routes.bp)
    app.register_blueprint(user_routes.bp)

    CORS(app)
    return app
