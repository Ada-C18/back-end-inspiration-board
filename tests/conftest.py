import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.user import User
from app.models.board import Board


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def saved_user(app):
    test_user = User(name="Test")
    db.session.add(test_user)
    db.session.commit()

@pytest.fixture
def two_saved_boards(app):
    db.session.add_all([
        User(name="Test"),
        Board(title="Hackspiration Board", user_id = 1, card_color = "black"),
        Board(title="Underwater Clown Board", user_id = 1, card_color = "black")
    ])
    db.session.commit()