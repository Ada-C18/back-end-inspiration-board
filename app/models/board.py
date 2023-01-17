from app import db
from app.models.card import Card

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy=True, passive_deletes=True)


    def to_dict(self, cards=False):
        if not self.cards and cards==False:
            return {
                'board_id': self.board_id,
                'title': self.title,
                'owner': self.owner
                }
        else:
            return {
                'board_id': self.board_id,
                'title': self.title,
                'cards': [card.to_dict() for card in self.cards],
                'owner': self.owner
                }
    @classmethod
    def from_dict_to_object(cls,data_dict):
        return cls(title=data_dict["title"], owner=data_dict['owner'])