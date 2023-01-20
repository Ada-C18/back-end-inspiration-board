from app import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))

    def to_dict(self):
        card_dict = {
            "id": self.id,
            "description": self.description,
            "like_count": self.like_count
        }
        return card_dict
