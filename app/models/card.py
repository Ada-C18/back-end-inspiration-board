from app import db
from flask import abort, make_response, jsonify

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship("Board", back_populates='cards')

    
    @classmethod
    def from_dict(cls, board_id, data_dict):
        return cls(message=data_dict["message"], likes_count=0, board_id=board_id)

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,
            "board": self.board.title
        }

    
    def update(self, req_body):
        try:
            self.message = req_body["message"]
        except KeyError:
            abort(make_response(jsonify(dict(details="Invalid data")), 400))