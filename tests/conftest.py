import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card
from flask.signals import request_finished


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
def one_board(app):
    board_1 = Board(title="Inspirational Quotes", owner="Tasha")

    db.session.add(board_1)

    db.session.commit()

@pytest.fixture
def two_boards(app):
    board_1 = Board(title="Motivational Quotes", owner="Tasha")
    board_2 = Board(title="Funny Quotes", owner="Tapasya")

    db.session.add(board_1)
    db.session.add(board_2)

    db.session.commit()

@pytest.fixture
def one_card(app):
    card_1 = Card(message = "Do your best")

    db.session.add(card_1)

    db.session.commit()

@pytest.fixture
def two_cards(app):
    card_1 = Card(message = "We've got this")
    card_2 = Card(message = "Practice makes perfect")

    db.session.add(card_1)
    db.session.add(card_2)

    db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)

    db.session.commit()

