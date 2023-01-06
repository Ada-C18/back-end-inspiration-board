import pytest
from app import create_app
from app.models.card import Card
from app.models.board import Board
from app import db
from flask.signals import request_finished

@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture gets called in every test that
# references "one_card"
# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(
        message="Go on my daily walk")
    db.session.add(new_card)
    db.session.commit()
