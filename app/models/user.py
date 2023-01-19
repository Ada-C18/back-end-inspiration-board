from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    boards = db.relationship("Board", back_populates="owner")
    cards = db.relationship("Card", back_populates="author")