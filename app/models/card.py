from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes = db.Column(db.Integer, default=None, nullable=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=True)
    board = db.relationship("Board", back_populates="cards", lazy=True)

    def from_instance_to_dict(self):
        instance_dict = {
            "id":self.card_id, 
            "message": self.message, 
            "likes": self.likes
            }
        return instance_dict

    @classmethod
    def from_dict_to_instance(cls, card_dict):
        try: 
            likes_count = card_dict["likes"]
        except KeyError:
            likes_count = 0

        return cls(
            message=card_dict["message"], 
            likes= likes_count
            )