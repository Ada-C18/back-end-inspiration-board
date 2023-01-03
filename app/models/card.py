from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id =  db.Column(db.Integer, db.ForeignKey('board.board_id'), default=None, nullable=False)
    board=db.relationship('Board', back_populates='cards')

    def dictionfy(self):
        return {
            'id':self.card_id,
            'message':self.message
        }

    @classmethod
    def create_card(cls,board_id,request_body):
        return Card(message=request_body['message'],board_id=board_id)
