from app import db
from flask import abort, make_response 

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String) 

    def to_dict_boards(self):
        return { "board":{
                "id":self.board_id,
                "title": self.title,
                "owner": self.owner}
                }

