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

# This fixture creates a board and saves it in the database
@pytest.fixture
def one_board(app):
    new_board = Board(
        title="test board 1",
        owner="QP/Lin"
    )
    db.session.add(new_board)
    db.session.commit()

#  This fixture creates four boards and saves them in the database
@pytest.fixture
def four_boards(app):
    db.session.add_all([
        Board(title="test board 1", owner="QP/Lin"),
        Board(title="test board 2", owner="QP/Lin"),
        Board(title="test board 3", owner="QP/Lin"),
        Board(title="test board 4", owner="QP/Lin"),
    ])
    db.session.commit()

# This fixture creates a card and saves it in the database
@pytest.fixture
def one_card(app):
    new_card = Card(message="test to get one card", likes_count=0, board_id=3)
    db.session.add(new_card)
    db.session.commit()


# This fixture creates a board and a card
# It associates the board and card, so that the
# board has this card, and the card belongs to one board
@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card = Card.query.first()
    board = Board.query.first()
    board.cards.append(card)
    db.session.commit()