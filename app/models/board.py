from app import db
from flask import make_response, abort

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)

    @classmethod
    def instance_from_json(cls, request_body):
        try:
            new_board = Board(title=request_body["title"],
            owner=request_body["owner"])
            return new_board
        except:
            abort(make_response({"details": "Invalid data"}, 400))
    
    def to_dict(self):
        return {
            "title": self.title,
            "owner": self.owner,
            "board_id": self.board_id,
        }

# @classmethod
# def instance_from_json(cls, request_body):
#     try:
#         new_board = Board(title=request_body["title"],
#         owner=request_body["owner"])
#         return new_board
#     except:
#         abort(make_response({"details": "Invalid data"}, 400))
