import pytest
from app import create_app
from app import db
from app.models.card import Card
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
def one_card(app):
    new_card = Card(message="It's friday!")
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def three_cards(app):
    db.session.add_all([Card(message="It's wednesday"),Card(message="It's Thursday"),Card(message="It's Saturday!")])
    db.session.commit()


@pytest.fixture
def one_board(app):
    new_board=Board(title="Days of the Week",owner="Mike")
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_card, one_board):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()


