from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, nullable=True)  # nullable = True okay?

    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=True)
    board = db.relationship("Board", back_populates="cards")

# When we create card we will set likes_count to 0

    def to_dict(self):
        return {"card_id": self.card_id,
                "message": self.message,
                "likes_count": self.likes_count,
                "board_id": self.board_id
                }
                
