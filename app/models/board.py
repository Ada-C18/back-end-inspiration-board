from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship('Card', back_populates='board')

    @classmethod
    def create_board(cls,request_body):
        return Board(title=request_body['title'], owner=request_body['owner'])