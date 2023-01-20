from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title =  db.Column (db.String, nullable = False)
    owner = db.Column(db.String, nullable = False)
    cards = db.relationship('Card', back_populates="board", lazy = True) #might need to change to back_ref
 
    def to_dict(self):
        board_dict = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
        }
        return board_dict