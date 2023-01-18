from app import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime)
    title = db.Column(db.String)
    visible = db.Column(db.Boolean)
    cards = db.relationship("Card", back_populates="board")
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner = db.relationship("User", back_populates="boards")
    card_color = db.Column(db.String)

    def to_dict(self):
        board_dict = {
            "id": self.id,
            "date_created": self.date_created,
            "title": self.title,
            "visible": self.visible,
            "owner": self.owner.name,
            "num_cards": (len(self.cards) if self.cards else 0)
        }
        if self.card_color:
            board_dict["card_color"] = self.card_color

        return board_dict

    @classmethod
    def from_dict(cls, board_data):
        new_board = Board( 
            date_created=board_data["date_created"],
            title=board_data["title"],
            visible=board_data["visible"],
            owner_id=board_data["owner_id"]
            )
            if board_data["card_color"]:
                new_board["card_color"] = board_data["card_color"]

        return new_board