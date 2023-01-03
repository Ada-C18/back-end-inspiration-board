from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board = db.relationship("Board", back_populates="cards")
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

    
    
    