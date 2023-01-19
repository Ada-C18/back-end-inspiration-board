from flask import Blueprint
from flask import abort, make_response # for error handling / represents current HTTP response
from flask import jsonify # for return formatting
from flask import request # represents current HTTP request
from app import db
from app.models.board import Board
from app.models.card import Card

# What routes are needed?
    # want to be able to GET: board + all its cards
        # /boards/<board_id>/cards
    # want to be able to POST: new board, new cards (attached to board)
        # /boards(new board)
        # /cards (new card)
    # want to be able to change (PATCH): board title, card title, description, liked status
        # /boards/<board_id>
        # /cards/<card_id>

    # want to be able to delete (DELETE): board - and all its cards, individual cards
        # /boards/<board_id>
        # /cards/<card_id>


# what data structures are needed?
    # Two tables: Boards and Cards
        # Cards: id, body, liked, board_id
        # Boards: id, title

# what data relationship is needed?
    # One-to-many (one board has many cards)

# Need to perform error handling (with validate function for board and card id)

hello_bp = Blueprint("homepage", __name__,url_prefix="/")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@hello_bp.route("", methods=["GET"])
def readme_page():
    return ("Welcome to our Inspiration Board API! Valid routes include /boards, /cards, /boards/board_id/cards and others!")

# CREATE A NEW CARD
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    new_card = Card(
        body=request_body["body"],
        likes=request_body["likes"],
        board_id=request_body["board_id"])

    db.session.add(new_card)
    db.session.commit()

    return ({
            "card_id":new_card.card_id,
            "body":new_card.body,
            "likes": 0,
            "board_id": new_card.board_id
        })

# GET ALL CARDS 
@cards_bp.route("", methods=["GET"])
def get_cards():
    all_cards = Card.query.all()
    card_list =[]
    for card in all_cards:
        card_list.append({
            "card_id":card.card_id,
            "body":card.body,
            "likes": card.likes,
            "board_id": card.board_id
        })
    return jsonify(card_list)

# GET CARD BY ID
@cards_bp.route("/<card_id>", methods=["GET"])
def get_card(card_id):
    card_id = int(card_id) 
    card = Card.query.get(card_id)
    return ({
        "card_id": card.card_id, 
        "body" : card.body,
        "likes": card.likes,
        "board_id": card.board_id})

# UPDATE CARD - LIKE STATUS, ETC
@cards_bp.route("/<card_id>", methods=["PATCH"])
def update_card(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    request_body = request.get_json()

    if request_body["body"]:
        card.body = request_body["body"]
    if request_body["likes"]:
        card.likes = request_body["likes"]
    if request_body["board_id"]:
        card.board_id = request_body["board_id"]

    db.session.commit()

    #return make_response(f"card '{card.card_id}' updated")
    return ({
        "card_id": card.card_id, 
        "body" : card.body,
        "likes": card.likes,
        "board_id": card.board_id})

# LIKE / UNLIKE CARD
@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def like_card(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    card.likes += 1

    db.session.commit()
    #return make_response(f"card '{card.card_id}' liked")
    return ({
        "card_id": card.card_id, 
        "body" : card.body,
        "likes": card.likes,
        "board_id": card.board_id})

@cards_bp.route("/<card_id>/unlike", methods=["PATCH"])
def unlike_card(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    card.likes -= 1

    db.session.commit()
    #return make_response(f"card '{card.card_id}' unliked")
    return ({
        "card_id": card.card_id, 
        "body" : card.body,
        "likes": card.likes, 
        "board_id": card.board_id})


# DELETE CARD
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(f"card '{card.card_id}' deleted")

# -----------------------------------------------------------------

# CREATE A NEW BOARD
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json() # retrieve body of HTTP request

    #create Board class object from request_body
    new_board = Board(title=request_body["title"])

    # add to database
    db.session.add(new_board)
    db.session.commit()

    return make_response(f"board '{new_board.title}' created")

# GET LIST OF ALL BOARDS
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    # retrieve all boards from database
    all_boards = Board.query.all()
    board_list = []
    for board in all_boards:
        board_list.append({
            "board_id" : board.board_id,
            "title": board.title,
        })
    return jsonify(board_list)

# GET BOARD INFO + ALL CARDS ASSOCIATED WITH BOARD
@boards_bp.route("/<board_id>/cards",methods=["GET"])
def get_board(board_id):
    #retrieve specific board from database
    board = Board.query.get(board_id)
    # create dictionary for return content
    board_dict = {}
    # create list for card content
    card_list = []
    # build card list
    for card in board.cards:
        card_dict = {
            "card_id": card.card_id,
            "body": card.body,
            "likes": card.likes
        }
        card_list.append(card_dict)
    board_dict["board_id"] = board.board_id
    board_dict["title"] = board.title
    board_dict["cards"] = card_list

    return board_dict

# UPDATE BOARD INFO
@boards_bp.route("/<board_id>", methods=["PATCH"])
def update_board(board_id):
    board = Board.query.get(board_id)
    request_body = request.get_json()

    board.title = request_body["title"]
    
    db.session.commit()

    return make_response(f"board '{board.title}' updated")

# DELETE BOARD
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = Board.query.get(board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response(f"board '{board.title}' deleted")




# ------------------ Practice Database and routes without postgres


# cards = [
#     {"id": 1, "body" : "Mexico", "liked": False, "board_id": 1},
#     {"id": 2, "body" : "Canada", "liked": False, "board_id": 1},
#     {"id": 3, "body" : "shopping", "liked": False, "board_id": 2},
#     {"id": 4, "body" : "Animal Farm", "liked": False, "board_id": 3},
# ]

# boards = [
#     {
#         "id": 1,
#         "title": "To visit"
#     },
#     {
#         "id": 2,
#         "title": "To do"
#     },
#     {
#         "id": 3,
#         "title": "To read"
#     },
# ]


# @boards_bp.route("/<board_id>",methods=["GET"])
# def get_board(board_id):
#     board_id = int(board_id)
#     for board in boards:
#         if board_id == board["id"]:
#             return ({
#                 "id": board["id"],
#                 "title" : board["title"]
#             })

# @boards_bp.route("/<board_id>",methods=["GET"])
# def get_board(board_id):
#     #retrieve specific board from database
#     board = Board.query.get(board_id)
#     for board in boards:
#         if board_id == board["id"]:
#             return ({
#                 "id": board["id"],
#                 "title" : board["title"]
#             })

# @boards_bp.route("/<board_id>/cards",methods=["GET"])
# def get_board_cards(board_id):
#     board_id = int(board_id)
#     card_list = []
#     for card in cards:
#         if board_id == card["board_id"]:
#             card_list.append(card)
#         for board in boards:
#             if board_id == board["id"]:
#                 board_info = {
#                     "id": board["id"],
#                     "title" : board["title"],
#                     "cards" : card_list
#                 }
#     return jsonify(board_info)

