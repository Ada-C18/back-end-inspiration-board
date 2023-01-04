from app import db
from datetime import datetime

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime)
    owner_id = db.Column(db.String, db.ForeignKey('user.id'))
    owner = db.relationship("Owner", back_populates="cards")
    likes = db.Column(db.Integer)
    message = db.Column(db.String)

    def to_dict(self):
        card_as_dict = {}
        card_as_dict["id"] = self.id
        card_as_dict["date_created"] = self.date_created
        card_as_dict["owner_id"] = self.owner_id
        card_as_dict["owner"] = self.owner
        card_as_dict["likes"] = self.likes
        card_as_dict["message"] = self.message
        

        return card_as_dict

    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(date_created=card_data["date_created"], owner=card_data["owner"], likes=card_data["likes"], message=card_data["message"])

        return new_card