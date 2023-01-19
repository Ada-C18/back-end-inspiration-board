from app import db


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        obj_dict = {
            "id": self.id,
            "title": self.title,
            "owner": self.owner
        }
        return obj_dict