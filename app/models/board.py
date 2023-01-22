from app import db

# Parent Model
class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }

    @classmethod
    def from_dict(cls, request_body):
        return cls (
            title= request_body["title"],
            owner= request_body["owner"]
        )