from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    def from_instance_to_dict(self, cards=False):
        instance_dict = {"id":self.board_id, "title": self.title, "owner": self.owner, "cards": self.cards}
        return instance_dict

    @classmethod
    def from_dict_to_instance(cls, board_dict):
        return cls(title=board_dict["title"], owner=board_dict["owner"])
