from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

def validate_models(cls, model_id):
  try:
    model_id = int(model_id)
  except:
    abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

  model = cls.query.get(model_id)

  if not model:
    abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
  return model

homepage_bp = Blueprint('homepage_bp', __name__)

@homepage_bp.route('/', methods=['GET'])
def read_homepage():
  return 'Welcome to our homepage!'

############################## BOARD ROUTES ##############################
boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')

# get all boards
@boards_bp.route('', methods=['GET'])
def read_boards():
  boards = Board.query.all()

  boards_response = []
  for board in boards:
    boards_response.append(
      {
        "board_id": board.board_id,
        "title": board.title,
        "owner": board.owner
      }
    )
  return jsonify(boards_response)

#get one board by board id
@boards_bp.route('/<board_id>', methods=['GET'])
def read_one_board(board_id):
  board = validate_models(Board, board_id)

  return{
      "board_id": board.board_id,
      "title": board.title,
      "owner": board.owner
  }

@boards_bp.route('/<board_id>', methods=["PUT"])
def update_board(board_id):
  board = validate_models(Board, board_id)

  request_body = request.get_json()

  board.title = request_body["title"]
  board.owner = request_body["owner"]

  db.session.commit()

  return make_response(jsonify("Board has been updated"))


# get one board by title instead of id, these two cannot be exist at the same time
# @boards_bp.route('/<title>', methods=['GET'])
# def read_one_board_with_title(title):
#   boards = Board.query.all()
#   for board in boards:
#     if board.title == title:
#       return {
#         "board_id": board.board_id,
#         "title": board.title,
#         "owner": board.owner
#       }
#   else:
#     return f"Board {title} not found!"

@boards_bp.route('', methods=['POST'])
def create_board():
  request_body = request.get_json()
  new_board = Board(
    title=request_body["title"],
    owner=request_body["owner"]
  )
  db.session.add(new_board)
  db.session.commit()

  return make_response(jsonify(f"Board {new_board.title} successfully created"), 201)

# delete board
@boards_bp.route('/<board_id>', methods=['DELETE'])
def delete_board(board_id):
  board = validate_models(Board, board_id)

  db.session.delete(board)
  db.session.commit()

  return make_response(jsonify(f"Board {board.board_id} successfully deleted"))

########################## CARD ROUTES ###################################
cards_bp = Blueprint('cards_bp', __name__, url_prefix='/cards')

# read all cards from one board
@boards_bp.route('/<board_id>/cards', methods=['GET'])
def read_cards(board_id):
  board = validate_models(Board, board_id)
  cards = Card.query.all()

  cards_response = []
  for card in cards:
    if card.board_id == board.board_id:
      cards_response.append(
        {
          "card_id": card.card_id,
          "message": card.message,
          "likes_count": card.likes_count
        }
      )
  return jsonify(cards_response)

# create card inside a board
@boards_bp.route('/<board_id>/cards', methods=['POST'])
def create_card(board_id):
  board = validate_models(Board, board_id)
  request_body = request.get_json()
  new_card = Card(
    message=request_body["message"],
    likes_count=request_body["likes_count"]
  )
  
  board.cards.append(new_card)
  db.session.add(new_card)
  db.session.commit()

  return make_response(jsonify(f"Card message {new_card.message} successfully created"), 201)


# update card likes count
@cards_bp.route('/<card_id>', methods=['PUT'])
def update_liked_card(card_id):
  card = validate_models(Card, card_id)
  card.likes_count = card.likes_count + 1

  db.session.commit()

  return make_response("Card like count has been updated successfully")

# DELETE card
@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_card(card_id):
  card = validate_models(Card, card_id)

  db.session.delete(card)
  db.session.commit()

  return make_response(jsonify(f"Card {card.card_id} successfully deleted"))