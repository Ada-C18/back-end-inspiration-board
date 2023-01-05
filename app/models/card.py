from app import db
# from app.routes_board import get_model_from_id
# from app.models.board import Board 

class Card(db.Model):
    card_id=db.Column(db.Integer, primary_key=True, autoincrement=True )
    message = db.Column(db.String)
    likes_count=db.Column(db.Integer)
    board_id= db.Column(db.Integer, db.ForeignKey('board.board_id'), default=None, nullable=True)
    board= db.relationship("Board", back_populates="cards")

    def add_likes(self):
        self.likes_count += 1

    def to_dict(self):
        card= {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }
        if self.board:
            card["board_id"] = self.board.board_id

        return card

    # def from_dict(card_data):
    #     if "board_id" not in card_data: 
    #         board = None
        
    #     else:
    #         board = get_model_from_id(Board, card_data["board_id"])
            

    #     return Card (
    #         message=card_data["message"],
    #         likes_count=0,
    #         board= board
    #     )
        