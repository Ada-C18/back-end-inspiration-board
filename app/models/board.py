from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String)
    owner=db.Column(db.String)
    cards=db.relationship("Card", back_populates="message")
    

# class Author(db.Model):
#   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#   name = db.Column(db.String)
#   books = db.relationship("Book", back_populates="author")


    def to_dict(self):
        board_dict = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,

        }
        if self.board_id:
            board_dict["board_id"] = self.board_id
        return board_dict

    @classmethod
    def from_dict(cls, board_dict):
        if "title" in board_dict and "owner" in board_dict:
            new_obj = cls(
            # board_id=board_dict["board_id"], 
            title=board_dict["title"], 
            owner= board_dict["owner"])
            
            return new_obj




