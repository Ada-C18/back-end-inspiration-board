from app import db


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy=True)

    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title=req_body["title"],
            owner=req_body["owner"]
        )



    def to_dict(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner 
        }

        if cards:
            board["cards"] = [card.to_dict() for card in self.cards]

        return board


