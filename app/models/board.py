from app import db
from app.models.card import Card

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship('Card', back_populates='board')

    def dictionfy(self):
        board_info =  {
            'id':self.board_id,
            'title':self.title,
            'owner':self.owner,
            'cards':[]
        }
        for card in self.cards:
            board_info['cards'].append(card.dictionfy())
        return board_info

    @classmethod
    def create_board(cls,request_body):
        return Board(title=request_body['title'], owner=request_body['owner'])
        