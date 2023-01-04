from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer , primary_key=True)
    author = db.Column(db.String)
    title= db.Column(db.String)
    messages = db.relationship("Card", back_populates="board")