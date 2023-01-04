from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    message = db.Column(db.String)
    likes = db.Column(db.String) 
    delete_status = db.Column(db.String, nullable = True)
    boards = db.relationship("Board", back_populates = "card", lazy = True)