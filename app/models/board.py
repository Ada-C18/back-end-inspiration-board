from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards= db.relationship("Card", back_populates="board")
    
    
    def to_dict(self):
        board_dict= {}
        board_dict["board_id"]= self.board_id
        board_dict["title"]= self.title
        board_dict["owner"]= self.owner
        
        return board_dict
    
    @classmethod
    def from_dict(cls, board_data):
        new_board= Board(title=board_data["title"],
                        owner=board_data["owner"])
        
        return new_board
    
    def update(self, req_body):
        try:
            self.title= req_body["title"]
            self.owner= req_body["owner"]
        except KeyError as error:
            raise error 