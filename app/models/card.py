from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    likes_count = db.Column(db.Integer)
    message = db.Column(db.String)
    board_id = db.Column(db.Integer, db.ForeignKey(
        'board.board_id'), nullable=True)
    board = db.relationship("Board", back_populates="cards", lazy=True)

    def create_dict(self):
        card_dict = {}
        card_dict["card_id"] = self.card_id
        card_dict["likes_count"] = self.likes_count
        card_dict["message"] = self.message
        card_dict["board_id"] = self.board_id
        return card_dict
