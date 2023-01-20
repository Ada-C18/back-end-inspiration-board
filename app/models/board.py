from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    owner = db.Column(db.String(40))
    cards = db.relationship("Card", back_populates="board")
