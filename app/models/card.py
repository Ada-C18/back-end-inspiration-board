from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=False)
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        result_dict = {}
        result_dict["card_id"] = self.card_id
        result_dict["message"] = self.message
        result_dict["likes"] = self.likes
        result_dict["board_id"] = self.board_id

        return result_dict

    @classmethod
    def from_dict(cls, data_dict):
        return cls(
            message=data_dict["message"],
            likes=data_dict["likes"]
        )

