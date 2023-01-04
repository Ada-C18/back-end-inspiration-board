from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(40))
    likes_count = db.Column(db.String)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        return dict(
            id=self.card_id,
            message=self.message,
            likes_count=self.likes_count,
            board_id=self.board_id,
        )

    @classmethod
    def from_dict(cls, card_data):
        new_card = cls(
            message=card_data["message"],
            likes_count=card_data["likes_count"],
            board_id=card_data["board_id"],
        )

        return new_card
