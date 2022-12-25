from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, nullable=True)  # nullable = True okay?

    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=True)
    board = db.relationship("Board", back_populates="cards")

# Questions: 
# default likes count??
#  

# Columns:

# card_id, int, primary key
# message, string
# likes_count, int
# board_id, int, foreign key to board_id in board

    def to_dict(self):
        dict = {"card_id": self.card_id,
                "message": self.message,
                "likes_count": self.likes_count,
                "board_id": self.board_id
                }
                

        return dict