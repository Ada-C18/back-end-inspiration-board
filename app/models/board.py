from app import db
# from app.models.card import Card

#ONE to many relationship
class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String) 
    cards = db.relationship("Card", back_populates="board", lazy=True)


    def to_dict(self):
        return {
            "title": self.title,
            "owner": self.owner,
            "id": self.board_id
        }


    @classmethod
    def from_dict(cls, request_body):
        return Board(
            title=request_body["title"],
            owner=request_body["owner"], 
        )





