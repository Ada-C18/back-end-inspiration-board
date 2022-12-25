from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.String(db.String) # do we want owner? 

    cards = db.relationship("Card", back_populates="board", lazy=True)

# Questions:
# do we want owner?


# Columns:

# board_id, int, primary key
# title, string
# owner, string

    def to_dict(self):
        return {"board_id": self.board_id,
                "title": self.title,
                "owner": self.owner,
                }

    @classmethod
    def from_dict(cls, data):
        return Board(title=data["title"], owner=data["owner"])
    
