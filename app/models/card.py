from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    message = db.Column(db.String)
    likes = db.Column(db.Integer, nullable = True) 
    delete_status = db.Column(db.String, nullable = True)
    boards = db.relationship("Board", back_populates = "card", lazy = True)

    @classmethod
    def from_json(cls, req_body):
        return cls(
            message = req_body["message"],
            likes = req_body["likes"],
            delete_status = req_body["delete_status"]
        )

    def to_dict_cards(self):
        return { "card":{
                "id":self.card_id,
                "message": self.message,
                "likes": self.likes,
                "delete_status": self.delete_status,
                }}
