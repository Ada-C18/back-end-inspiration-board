from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    
    
    
    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title=req_body["title"],
            owner=req_body["owner"]
        )