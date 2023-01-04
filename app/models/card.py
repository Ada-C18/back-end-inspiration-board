from app import db
from flask import abort, make_response


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=True)
    board = db.relationship("Card", back_populates="cards")

    def to_json(self):
        card_as_json = {}
        card_as_json["id"] = self.card_id
        card_as_json["message"] = self.message
        card_as_json["likes_count"] = self.likes_count
        return card_as_json

    @classmethod
    def from_json(cls, card_json):
        if "message" in card_json and len(card_json["message"]) <= 40:
            new_obj = cls(message=card_json["message"])
            return new_obj
        else:
            abort(make_response({"Invalid data": "Message cannot be blank or more than 40 characters"}, 400))
