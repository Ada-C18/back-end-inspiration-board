from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        return dict(
            board_id = self.board_id,
            title = self.title,
            owner = self.owner,
            cards = self.cards
        )
    
    @classmethod
    def from_json(cls, board_data):
        new_board = Board(
            title=board_data["title"],
            owner=board_data["owner"]
        )
        return new_board