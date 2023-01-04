from app import db

class Board(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    author = db.Column(db.String)
    title= db.Column(db.String)
    cards = db.relationship("Card", back_populates="board") 