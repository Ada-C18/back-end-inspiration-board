from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
<<<<<<< HEAD


    def to_dict(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner 
        }


=======
    
    
    
    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title=req_body["title"],
            owner=req_body["owner"]
        )
>>>>>>> 017f7b4cf16f59f84eeac4b99eacfe570b1a59be
