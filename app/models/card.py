from app import db
from datetime import datetime

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime)
    card_title = db.Column(db.String)
    visible = db.Column(db.Boolean)
    card_owner = db.Column(db.String, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="boards")

    def to_dict(self):
        card_as_dict = {}
        card_as_dict["id"] = self.id
        card_as_dict["date_created"] = self.date_created
        card_as_dict["card_title"] = self.card_title
        card_as_dict["visible"] = self.visible

        return card_as_dict

    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(date_created=card_data["date_created"], card_title=card_data["card_title}]"], card_owner=card_data["card_owner"], visible=card_data["visible"])

        return new_card