from app import db
from flask import Blueprint, request, jsonify, make_response, abort

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board = db.relationship("Board", back_populates = "cards")
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
        }

    @classmethod
    def from_dict(cls, cls_dict):
        if "message" in cls_dict and "likes_count" in cls_dict:
            validate_message_is_not_empty_string(cls_dict)

            return cls(message = cls_dict["message"], likes_count = cls_dict["likes_count"])

        elif "message" in cls_dict:
            validate_message_is_not_empty_string(cls_dict)

            return cls(message = cls_dict["message"])
        else:
            response_str = "missing necessary information"
            abort(make_response(jsonify({"message":response_str}), 404))


def validate_message_is_not_empty_string(dict):
    if dict["message"] == "":
        response_str = "please enter a message"
        abort(make_response(jsonify({"message":response_str}), 404))


