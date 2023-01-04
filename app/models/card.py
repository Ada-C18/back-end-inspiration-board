from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

    def to_dict(self):
        if self.card_id:
            return {
                "id":self.card_id,
                "message":self.card.message,
                "likes":self.card.likes_count
            }