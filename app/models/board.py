from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    owner=db.Column(db.String)

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
        if "board_id" in board_dict  and "title" in board_dict and "owner" in board_dict:
            new_obj = cls(
            # board_id=board_dict["board_id"], 
            title=board_dict["title"], 
            owner= board_dict["owner"])
            
            return new_obj




