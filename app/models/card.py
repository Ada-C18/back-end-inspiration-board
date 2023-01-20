from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=False)
    board = db.relationship("Board", back_populates="cards")

    @db.validates("message")
    def no_empty_strings(self, key, value):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{key} must be a non-empty string.")
        return value

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,
        }

    @classmethod
    def filter_data(cls, board_data):
        accepted_data = ("message", "board_id")
        return {field: board_data[field] for field in accepted_data}

    @classmethod
    def from_dict(cls, card_data):
        return Card(**Card.filter_data(card_data))
