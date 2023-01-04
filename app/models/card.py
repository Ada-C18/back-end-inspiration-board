from app import db

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
        return cls(message = cls_dict["message"])

