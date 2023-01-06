from flask import Blueprint, request, jsonify, make_response,abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

def validate_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message":f"{cls.__name__} #{model_id} is invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} #{model_id} not found"}, 404))

    return model


@boards_bp.route('', methods=['GET'])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append(
            {
                "id": board.id,
                "title": board.title,
                "owner": board.owner,
                "cards": [card.to_dict() for card in board.cards]
            }
        )
    return jsonify({"boards": board_response}), 200


@boards_bp.route("", methods=['POST'])
def create_a_board():
    request_body= request.get_json()
    try:
        new_board = Board(title=request_body["title"],
            owner=request_body["owner"], cards=[])
    except:
        abort(make_response({'details': f'Title and owner are required'}, 400))

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict()), 201


@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_id(Board,id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify({"details": f'Board #{id} "{board.title}" was successfully deleted'}), 200)


# <-----------------------Cards--------------------->

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_a_card(board_id):
    validate_id(Board, board_id)
    request_body = request.get_json()

    try:
        new_card = Card(message=request_body["message"], likes_count=0,
                    board_id=board_id)

    except:
        abort(make_response({'details': f'Title and owner are required'}, 400))

    db.session.add(new_card)
    db.session.commit()

    return jsonify(new_card.to_dict()), 201


@boards_bp.route("/<board_id>/cards/<card_id>", methods=["PATCH"])
def like_card(board_id, card_id):
    board = validate_id(Board, board_id)

    # for card in board.cards:
    #     if card.id == card_id:
    #         card.likes_count += 1
    
    response = [card.to_dict() for card in board.cards if card.id == card_id]

    db.session.commit()

    return make_response(jsonify(response), 200)


@boards_bp.route("<board_id>/cards/<id>", methods=["DELETE"])
def delete_card(id):
    card = validate_id(Card, id)

    db.session.delete(card)
    db.session.commit()

    return make_response(f"Card #{id} was successfully deleted"),200


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_from_one_board(board_id):
    board = validate_id(Board, board_id)
    board_cards = [card.to_dict() for card in board.cards]
    
    return jsonify({"cards":board_cards}), 200