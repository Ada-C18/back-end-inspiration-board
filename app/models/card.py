from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(40))
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        return dict(
            card_id = self.card_id,
            message = self.message,
            likes_count =self.likes_count
        )

    @classmethod
    def from_dict(cls, card_data):
        the_card = cls(
            message = card_data["message"]
        
        )

        return the_card


# likes_count ?

    