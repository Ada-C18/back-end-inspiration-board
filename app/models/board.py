from app import db
from flask import abort, make_response 

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String) 

    @classmethod
    def from_json(cls, req_body):
        return cls(
            title = req_body["title"],
            owner = req_body["owner"]
        )



    def to_dict_boards(self):
        return { "board":{
                "id":self.board_id,
                "title": self.title,
                "owner": self.owner}
                }

