from os import abort
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


# helper function
def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400)) 

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404)) 

    return model



################################################################
###################### BOARD ROUTES ############################

# create a post route //works!
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.from_json(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_board)
    db.session.commit()

    return make_response(new_board.to_dict_boards(), 201)

# create a get one board route //works!
@boards_bp.route("/<board_id>", methods = ["GET"])
def get_one_board(board_id):
    board = validate_model(Board, board_id)

    return jsonify(board.to_dict_boards(), 200)

# create get all route //works!
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    boards_response = []
    boards = Board.query.all()
    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        })

    return jsonify(boards_response)

# create a route to delete all boards # works

@boards_bp.route("", methods=["DELETE"])
def delete_board():
    boards = Board.query.all()
    for board in boards:
        db.session.delete(board)
        db.session.commit()


    deleted_board_dict = {"details":f"Boards successfully deleted"}

    return make_response(jsonify(deleted_board_dict), 200)

#create a post route for card # works 
# @cards_bp.route("", methods = ["POST"])
# def create_card():
#     request_body = request.get_json()
#     try:
#         new_card = Card.from_json(request_body)
#     except KeyError:
#         return make_response({"details": "Invalid data"}, 400)
#     db.session.add(new_card)
#     db.session.commit()
#     return make_response(new_card.to_dict_cards(), 201)

# create a post route to assign card to board //works!

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def assign_card_to_board(board_id):


    board = validate_model(Board, board_id) 
    request_body = request.get_json()

    try:
        new_card = Card.from_json(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_card)
    db.session.commit()
    board.cards.append(new_card)

    db.session.add(board)
    db.session.commit() 
    
    return make_response(new_card.to_dict_cards(), 201)
    # board.cards = [] 

    # needs to accept a dictionary of card data,
    # may need to combine single card post route with this route


    # for card in request_body['cards']:
    #     card = validate_model(Card, card)

    #board.append(new_car)

    # board.cards.append(new_card)

    

# create a get route to see all card of a board //works!

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def gets_cards_of_one_board(board_id):

    board = validate_model(Board, board_id)
    cards_of_board =[]  
    
    for card in board.cards:
        cards_of_board.append(
            {
                "id": card.card_id,
                "board_id": card.board_id,
                "message": card.message,
                "likes": card.likes,
            }
            ) 
    return make_response(jsonify({"id":board.board_id,"title":board.title,"cards":cards_of_board})),200 



################################################################
####################### CARD ROUTES ############################





#create a get all cards route # works
@cards_bp.route("", methods = ["GET"])
def get_all_cards():
    cards_response = []
    cards = Card.query.all()
    for card in cards:
        cards_response.append({
            "id": card.card_id,
            "message": card.message,
            "likes": card.likes
        })

    return jsonify(cards_response)



# create a route to delete a single card #works
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card,card_id)

    db.session.delete(card)
    db.session.commit()
    deleted_card_dict = {"details":f"Card {card.card_id} \"{card.message}\" successfully deleted"}

    return make_response(jsonify(deleted_card_dict), 200)



# make a patch route to increase likes count //works!
@cards_bp.route("/<card_id>", methods=["PATCH"])
def add_likes(card_id):
    card = validate_model(Card, card_id)

    card.likes += 1

    db.session.commit()

    return make_response(jsonify({"id":card.card_id,"likes": card.likes})),200 





