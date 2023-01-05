from app import db

class Card(db.Model):
    card_id= db.Column(db.Integer, primary_key=True)
    message= db.Column(db.String)
    likes_count= db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # title = db.Column(db.String)
    # description = db.Column(db.String)
    # author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    # author = db.relationship("Author", back_populates="books")

    def to_dict(self):
        card_dict = {
            "card_id" : self.card_id,
            "message" : self.message,
            "likes_count" : self.likes_count
        }
        if self.card_id:
            card_dict["card_id"] = self.card_id

        return card_dict

    @classmethod
    def from_dict(cls, data_dict):
        if "message" in data_dict :
            new_obj = cls(
                message = data_dict["message"])
            return new_obj
# def to_dict(self):
#         task_dict = {
#         "id": self.task_id,
#         "title": self.title,
#         "description": self.description,
#         "is_complete": False if self.completed_at is None else True
#         }
#         if self.goal_id:
#             task_dict["goal_id"] = self.goal_id

#         return task_dict

    
#     @classmethod
#     def from_dict(cls, data_dict):
#         if "title" in data_dict  and "description" in data_dict and "is_complete" in data_dict:
#             new_obj = cls(
#             title=data_dict["title"], 
#             description=data_dict["description"], 
#             is_complete= data_dict["is_complete"])
            
#             return new_obj


