from app import db
# from app.models.board import Board

# one to MANY relationship
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board = db.relationship("Board", back_populates="cards")


    def to_dict(self):
        card_as_dict = {}
        card_as_dict["id"] = self.card_id
        card_as_dict["message"] = self.message
        card_as_dict["likes_count"] = self.likes_count
        card_as_dict["board_id"] = self.board_id

        return card_as_dict

    @classmethod
    def from_dict(cls, request_body,):
        return Card(
            message=request_body["message"],
            likes_count=request_body["likes_count"]
        )
    