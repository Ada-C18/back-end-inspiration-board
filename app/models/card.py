from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    board = db.relationship("Board", back_populates="cards", lazy=True)
    # an object from the card class can accept a relationship from an object 
    # that's from the Board class. backpopulates signals that the specific board 
    # object will now display this specific card in its board.cards attribute
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id', ondelete='CASCADE'), nullable=True)
    likes_count = db.Column(db.Integer, default=0)

    def to_dict(self):
        card_as_dict = {}
        card_as_dict["card_id"] = self.card_id
        card_as_dict["message"] = self.message
        card_as_dict["likes_count"] = self.likes_count
        card_as_dict["board_id"] = self.board_id
        return card_as_dict
    @classmethod
    def from_dict_to_object(cls,data_dict):
        return cls(message=data_dict["message"])



    