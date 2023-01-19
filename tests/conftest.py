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


# This fixture creates two boards and saves it in the test database
@pytest.fixture
def two_boards(app):
    first_board = Board(
        title="Our inspo board", owner="JJ")
    second_board = Board(
        title="Aspirations", owner="Team Serval")
    
    db.session.add(first_board)
    db.session.add(second_board)
    db.session.commit()


@pytest.fixture
def board_with_cards(app):
    board = Board(title="Our inspo board", owner="JJ")
    first_card = Card(message="This is a card", likes_count=0, board_id=1)
    second_card = Card(message="Second card", likes_count=0, board_id=1)

    db.session.add(board)
    board.cards.append(first_card)
    board.cards.append(second_card)
    db.session.commit()
