from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String) 
    owner = db.Column(db.String)
    cards = db.relationship('Card', back_populates='board')

    def to_dict(self):
        return {
            "id":self.board_id,
            "title":self.title,
            "owner":self.owner
        }

    def to_dict_card(self):
        return {
        "id":self.board_id,
        "title":self.title,
        "owner":self.owner,
        "cards":self.get_card_list()
        }
    
    def get_card_list(self):
        list_of_cards = []
        for item in self.cards:
            list_of_cards.append(item.to_dict())
        
        return list_of_cards