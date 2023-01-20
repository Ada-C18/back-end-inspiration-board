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


### creating model tables for our tests ###
@pytest.fixture
def one_board(app):
    example_board = Board(
        title="This is an inspiration board",
        owner="Curious Georges"
    )
    db.session.add(example_board)
    db.session.commit()


@pytest.fixture
def one_card_on_one_board(app, one_board):
    example_board = Board.query.first()
    example_card = Card(
        message="This is an inspirational card",
        board_id=1,
        likes_count=0
    )
    db.session.add_all([example_board, example_card])
    db.session.commit()


@pytest.fixture
def two_cards_on_two_boards(app, one_card_on_one_board):
    second_board = Board(
        title="This is a second inspiration board",
        owner="Caitlyn"
    )
    db.session.add(second_board)

    second_card = Card(
        message="Hope you're having a great day!",
        board_id=2,
        likes_count=0
    )
    db.session.add(second_card)
    db.session.commit()
