from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        cards_list = [card.to_dict() for card in self.cards]
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": cards_list
        }

    @classmethod
    def from_dict(cls, cls_dict):
        return cls(title = cls_dict["title"], owner = cls_dict["owner"])
