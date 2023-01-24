from app import db


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship('Card', back_populates='board', lazy=True)    
    
    def to_dict(self):
        dict = {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner
            
        }
        return dict
    
    def to_dict_relationship(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": self.get_cards_list()
            
        }
    
    
    def get_cards_list(self):
        list_of_cards = []
        for card in self.cards:
            list_of_cards.append(card.to_dict())
        return list_of_cards