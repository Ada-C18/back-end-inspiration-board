from app import db
from flask import make_response, abort

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id")) #nullable=False is implied (board is required)
    board = db.relationship("Board", back_populates="cards")

    @classmethod
    def instance_from_json(cls, request_body, board_id):
        try:
            new_card = Card(message=request_body["message"], board_id=board_id, likes_count=0)
            return new_card
        except:
            abort(make_response({"details": "Invalid data"}, 400))

    def to_dict(self):
        return {
            "message": self.message,
            "likes_count": self.likes_count,
            "card_id": self.card_id,
            "board_id": self.board_id
        }
        