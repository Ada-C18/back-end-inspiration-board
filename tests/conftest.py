import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card


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
def create_one_board(app):
    new_board = Board(title="Kitty Treats", owner="Grumpy Cat")
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def create_four_boards(app):
    db.session.add_all([
        Board(title="Cats", owner="Grumpy Cat"),
        Board(title="Dogs",owner="Snoopy"),
        Board(title="Birds",owner="Toucan"),
        Board(title="Rabbits",owner="Jumper")
    ])
    db.session.commit()

@pytest.fixture
def create_four_cards_associated_with_a_board(app, create_one_board):
    db.session.add_all([
        Card(message="Message #1", board_id=1),
        Card(message="Card #2", board_id=1),
        Card(message="Hello World", board_id=1),
        Card(message="hello hello", board_id=1)
    ])
    db.session.commit()

@pytest.fixture
def create_one_card(app, create_one_board):
    new_card = Card(message="testing testing 123", board_id=1)
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def create_card_with_likes(app, create_one_board):
    new_card = Card(message="testing testing 123", likes_count=30, board_id=1)
    db.session.add(new_card)
    db.session.commit() 