import pytest
from app import create_app
from app import db
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
def three_boards(app):
    db.session.add_all([
        Board(
            title="Inspirational Quotes",
            owner="Cristal",
            # cards=[],
        ),
        Board(
            title="To-do",
            owner="Annie",
            # cards=[],
        ),
        Board(
            title="Thoughts",
            owner="Cristal",
            # cards=[],
        ),
    ])
    db.session.commit()

@pytest.fixture
def one_board(app):
    new_board = Board(
        title="Inspiration",
        owner="Cristal",
        cards=[{
                "board_id": 1,
                "id": 1,
                "likes_count": 54,
                "message": "does this return an int"
            },
            {
                "board_id": 1,
                "id": 2,
                "likes_count": 0,
                "message": "we're testing more"
            },
            {
                "board_id": 1,
                "id": 3,
                "likes_count": 17,
                "message": "lots of cards"
            },
            {
                "board_id": 1,
                "id": 4,
                "likes_count": 20,
                "message": "no sql databases"
            },
            {
                "board_id": 1,
                "id": 5,
                "likes_count": 6,
                "message": "no concept of migrations"
            }],
    )
    db.session.add(new_board)
    db.session.commit()