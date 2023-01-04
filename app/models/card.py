from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship('Board', back_populates='cards')
    
    def to_dict(self):
        dict = {
            "id": self.card_id,
            "message": self.message,
            "likes_count": 0,
            
        }
        return dict