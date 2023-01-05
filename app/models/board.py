from app import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime)
    title = db.Column(db.String)
    visible = db.Column(db.Boolean)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        board_as_dict = {
            "id": self.id,
            "date_created": self.dated_created,
            "title": self.title,
            "visible": self.visible,
        }
        return board_as_dict

    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(date_created=board_data["date_created"], 
            title=board_data["title"], 
            visible=board_data["visible"])

        return new_board