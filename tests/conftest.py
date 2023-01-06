import pytest
from app import create_app
from app import db
from app.models.board import Board


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

@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(
            title="Inspirational Quotes",
            owner="Cristal",
            # cards=[],
        ),
        Board(
            title="To-do",
            owner="Annie",
            # cards=[],
        ),
        Board(
            title="Thoughts",
            owner="Cristal",
            # cards=[],
        ),
    ])
    db.session.commit()
