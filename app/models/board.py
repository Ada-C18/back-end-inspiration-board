from app import db
from datetime import datetime

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime)
    title = db.Column(db.String)
    visible = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship("Owner", back_populates="boards")

    def to_dict(self):
        board_as_dict = {
            "id": self.id,
            "date_created": self.dated_created,
            "title": self.title,
            "visible": self.visible,
            "owner": self.owner.name
        }
        return board_as_dict

    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(date_created=board_data["date_created"], 
            title=board_data["title"], 
            owner=board_data["owner"], 
            visible=board_data["visible"])

        return new_board