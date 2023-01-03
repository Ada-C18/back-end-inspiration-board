from app import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner_name = db.Column(db.String, nullable=False)
    cards = db.relationship("Card", back_populates="board")


    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title=board_data["title"],
                    owner_name=board_data["owner_name"])
        return new_board