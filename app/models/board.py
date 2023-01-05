from app import db

class Board(db.Model):
    
    board_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates = "board")

    def to_dict(self):
        return dict(
            id = self.board_id,
            title = self.title,
            owner = self.owner
        )

    @classmethod
    def from_dict(cls, board_data):
        return cls(
            title=board_data["title"],
            owner=board_data["owner"]
        )