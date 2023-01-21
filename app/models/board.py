from app import db
from flask import abort, make_response


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy=True)

    def to_json(self):
        board_as_json = {}
        board_as_json["id"] = self.board_id
        board_as_json["title"] = self.title
        board_as_json["owner"] = self.owner
        return board_as_json

    @classmethod
    def from_json(cls, board_json):
        if board_json.get("title") and board_json.get("owner"):
            new_obj = cls(title=board_json["title"], owner=board_json["owner"])
            return new_obj
        else:
            abort(make_response({"Invalid data": "Board title or owner's name cannot be blank"}, 400))

