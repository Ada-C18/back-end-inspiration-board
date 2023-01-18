from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime)
    likes = db.Column(db.Integer)
    message = db.Column(db.String)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship("Board", back_populates="cards")
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="cards")

    def to_dict(self):
        card_dict = {
            "id": self.id,
            "date_created": self.date_created,
            "likes": self.likes,
            "message": self.message,
            "author_id": self.author_id,
        }
        
        if self.board:
            card_dict["board_id"] = self.board.id

        return card_dict

    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(
            date_created=card_data["date_created"],
            likes = card_data["likes"], 
            message = card_data["message"],
            board_id = card_data["board_id"],
            author_id = card_data["author_id"])

        return new_card