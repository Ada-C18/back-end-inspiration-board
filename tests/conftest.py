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
        message="You are doing great!")
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def three_cards(app):
    db.session.add_all([
        Card(
            message="You are powerful"
        ),
        Card(
            message="Today is going to be a good day"
        ),
        Card(
            message="The stars want you to be successful"
        )
    ])   
    
    db.session.commit()

@pytest.fixture
def one_board(app):

    new_board = Board(title="January Board", author="r")
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()



