from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        return dict(
            card_id = self.card_id,
            message = self.message,
            likes_count = self.likes_count,
            board_id = self.board_id
        )

    @classmethod
    def from_json(cls, card_data):
        new_card = Card(
            message = card_data["message"],
        )
        return new_card
