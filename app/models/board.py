from app import db
from datetime import datetime

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime)
    board_title = db.Column(db.String)
    visible = db.Column(db.Boolean)
    board_owner = db.Column(db.String, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="boards")

    def to_dict(self):
        board_as_dict = {}
        board_as_dict["id"] = self.id
        board_as_dict["date_created"] = self.date_created
        board_as_dict["board_title"] = self.board_title
        board_as_dict["visible"] = self.visible

        return board_as_dict

    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(date_created=board_data["date_created"], board_title=board_data["board_title}]"], board_owner=board_data["board_owner"], visible=board_data["visible"])

        return new_board