from app import db

class Board(db.Model):
    board_id=db.Column(db.Integer, primary_key=True, autoincrement=True )
    title = db.Column(db.String)
    owner=db.Column(db.String)
    cards=db.relationship("Card", back_populates="board")

    def to_dict(self):
        board= {
            "board_id":self.board_id,
            "title": self.title,
            "owner":self.owner
        }
        if self.cards:
            board["cards"]= [card.to_dict() for card in self.cards]
        else: 
            board['cards'] = []


        return board 

    def from_dict(board_data):
        return Board (
            title=board_data["title"],
            owner=board_data["owner"]
        )

