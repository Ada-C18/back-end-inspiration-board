import pytest
from app import create_app
from app.models.board import Board
from app.models.card import Card
from app import db
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
    """Creates an app with an empty database."""
    return app.test_client()


@pytest.fixture
def one_board(app):
    """Creates an app with one board and no cards."""
    db.session.add(
        Board(name="Test Board", owner="Test Owner")
    )
    db.session.commit()

@pytest.fixture
def one_board_three_cards(one_board):
    """Creates an app with one board and three cards."""
    board = Board.query.first()
    db.session.add_all([
        Card(board_id=board.board_id, message="Hello", likes_count=0),
        Card(board_id=board.board_id, message="Test", likes_count=1),
        Card(board_id=board.board_id, message="Goodbye", likes_count=2),
    ])
    db.session.commit()
