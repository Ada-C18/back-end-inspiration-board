from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id =  db.Column(db.Integer, db.ForeignKey('board.board_id'), default=None, nullable=True)
    board=db.relationship('Board', back_populates='cards')
