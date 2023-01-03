from app import db

class Card(db.Model):
    card_id=db.Column(db.Integer, primary_key=True, autoincrement=True )
    message = db.Column(db.String)
    likes_count=db.Column(db.Integer)

    def add_likes(self):
        self.likes_count += 1

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }

    def from_dict(card_data):
        return Card (
            message=card_data["message"],
            likes_count=0
        )