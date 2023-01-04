from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    description = db.Column(db.String, nullable = False)
    like_count = db.Column(db.Integer)
    board = db.relationship('Board', back_populates="card", lazy = True)