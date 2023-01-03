from app import db

class Board(db.model):
    
    board_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    owner = db.Column(db.String)

    def to_dict(self):
        return dict(
            id = self.board_id,
            title = self.title,
            owner = self.owner
        )