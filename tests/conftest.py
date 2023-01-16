import pytest
from app import create_app
from app.models.board import Board
from app.models.card import Card
from app import db


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

# This fixture creates a task and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(
        title="test board 1",
        owner="QP/Lin"
    )
    db.session.add(new_board)
    db.session.commit()

#  This fixture creates four tasks and saves them in the database
@pytest.fixture
def four_boards(app):
    db.session.add_all([
        Board(title="test board 1", owner="QP/Lin"),
        Board(title="test board 2", owner="QP/Lin"),
        Board(title="test board 3", owner="QP/Lin"),
        Board(title="test board 4", owner="QP/Lin"),
    ])
    db.session.commit()

# This fixture creates a goal and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(message="test to get the third card", likes_count=0)
    db.session.add(new_card)
    db.session.commit()
