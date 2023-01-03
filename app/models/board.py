from app import db
class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    # owner = db.relationship("Task", back_populates="goal")

    def to_dict(self):
            return {
                "title": self.goal_id,
                "owner": self.title
            }