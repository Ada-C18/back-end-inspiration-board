from app import db


class Board (db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy=True)

    def to_dict(self):
        board_dict = {
            'id': self.board_id,
            'title': self.title,
            'owner': self.owner,
        }
        if self.cards == []:
            board_dict["cards"] = []
        else:
            board_dict['cards'] = [card.to_dict() for card in self.cards]

        return board_dict
