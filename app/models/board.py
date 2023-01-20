from app import db

from random import randint


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    color = db.Column(db.Integer, default=lambda: randint(0, 256**3), nullable=False)
    cards = db.relationship("Card", back_populates="board")

    @db.validates("title", "owner")
    def no_empty_strings(self, key, value):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{key} must be a non-empty string.")
        return value

    @db.validates("color")
    def color_24bit(self, key, value):
        colorError = ValueError(f"{key} must represent a 24-bit color.")

        if isinstance(value, str):
            value = "".join(filter(lambda v: v in "0123456789abcdefABCDEF", value))
            value = int(value, 16)

        if value is None:
            return randint(0, 256**3)

        if isinstance(value, int):
            if value < 0 or value > (256**3):
                raise colorError
            return value

        raise colorError

    def to_dict(self, color=False):
        board_dict = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
        }
        if color:
            board_dict["color"] = f"#{self.color:0>6X}"
        return board_dict

    @classmethod
    def filter_data(cls, board_data):
        accepted_data = ("title", "owner")
        return {field: board_data[field] for field in accepted_data}

    @classmethod
    def from_dict(cls, board_data):
        return Board(**Board.filter_data(board_data))

    def update(self, board_data):
        for field, value in Board.filter_data(board_data).items():
            setattr(self, field, value)

    def set_color(self, color):
        self.color = color
