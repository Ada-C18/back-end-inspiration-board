from flask import Blueprint, request, jsonify, make_response,abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Board validation helper function
def validate_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message":f"{cls.__name__} {id} is invalid"}, 400))

    model = cls.query.get(id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} #{id} not found"}, 404))

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
                "cards": board.cards,
            }
        )
    return jsonify(board_response)

@ boards_bp.route('', methods=['POST'])
def create_a_board():
    request_body= request.get_json()
    try:
        new_board = Board(title=request_body["title"],
            owner=request_body["owner"])
    except:
        abort(make_response({'details': f'Title and owner are required'}, 400))

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"Board {new_board.title} was successfully created", 201)

@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_id(Board,id)

    db.session.delete(board)
    db.session.commit()

    return make_response(f"Board #{id} {board.title} was successfully deleted"),200


# <-----------------------Cards--------------------->


@cards_bp.route("/<id>", methods=["PATCH"])
def like_card(id):
    card = validate_id(Card, id)
    card.likes_count += 1
    db.session.commit()
    return make_response(jsonify(card.to_dict()), 200)


@cards_bp.route("/<id>", methods=["DELETE"])
def delete_Card(id):
    card = validate_id(Card, id)

    db.session.delete(card)
    db.session.commit()

    return make_response(f"Card #{id} was successfully deleted"),200
