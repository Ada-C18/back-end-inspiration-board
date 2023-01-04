from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    message = db.Column(db.String(140))
    likes_count = db.Column(db.Integer, default=0)
    board = db.relationship("Board", back_populates="cards")
