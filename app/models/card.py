from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board = db.relationship("Board", back_populates="cards")
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

    def to_dict(self):
        card_as_dict = {}
        card_as_dict["id"] = self.card_id
        card_as_dict["likes_count"] = self.likes_count
        card_as_dict["message"] = self.message

        return card_as_dict