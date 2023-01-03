from app import db
from flask import abort, make_response, jsonify

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String)

    # Create new board
    @classmethod
    def from_dict(cls, request_body):
        return cls(title=request_body["title"], owner=request_body["owner"])

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "owner": self.owner,
        }

    # Update board
    def update(self, request_body):
        try:
            self.title = request_body["title"]
            self.owner = request_body["owner"]
        except KeyError:
            abort(make_response(jsonify(dict(details="Invalid data")), 400))

    

    