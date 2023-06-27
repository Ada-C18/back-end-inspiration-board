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
def quotes_board(app):
    quotes_board = Board(title="Inspirational Quotes", owner="Jamal")

    db.session.add(quotes_board)

@pytest.fixture
def reading_list_board(app):
    reading_list_board = Board(title="Books to Read", owner="Sophie")

    db.session.add(reading_list_board)

@pytest.fixture
def two_boards(app, quotes_board, reading_list_board):
    db.session.add_all([quotes_board, reading_list_board])

@pytest.fixture
def two_boards(app):
    quotes_board = Board(title="Inspirational Quotes", owner="Jamal")
    reading_list_board = Board(title="Books to Read", owner="Sophie")

    db.session.add_all([quotes_board, reading_list_board])

def three_cards(app, two_boards):
    quote1 = Card(message="Reach for the stars", board=two_boards[0])
    quote2 = Card(message="You can do it!", board=two_boards[0])
    quote3 = Card(message="The Name of the Rose", board=two_boards[1])

    db.session.add_all([quote1, quote2, quote3])