from app import db
from flask import abort, make_response

# Child model
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board= db.relationship("Board", back_populates="cards")
    
   
    def to_dict(self):
        return {
            "id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id
        }
    
    @classmethod 
    
    def from_dict(cls, request_body):
        return cls(
            
            message= request_body["message"],
            likes_count= request_body["likes_count"],
            board_id= request_body["board_id"]
        )

