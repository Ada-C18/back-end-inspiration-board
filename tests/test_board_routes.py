from werkzeug.exceptions import HTTPException
from app.models.board import Board
import pytest


def test_get_all_boards_with_no_records(client):
    pass

def test_get_all_boards_with_three_records(client, three_boards):
    pass

def test_get_one_board_with_missing_record(client, three_boards):
    pass

def test_get_one_board(client, three_boards):
    pass

def test_create_one_board(client):
    pass

def test_create_one_board_no_title(client):
    pass

def test_create_one_board_no_owner(client):
    pass