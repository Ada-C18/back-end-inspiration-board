from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    # specify card_id and change board_id
    description = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board = db.relationship('Board', back_populates="cards", lazy=True)

    def to_dict(self):
        card_dict = {
            "card_id": self.card_id,
            "description": self.description,
            "like_count": self.like_count
        }
        return card_dict
