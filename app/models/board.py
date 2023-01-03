from app import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner_name = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")
