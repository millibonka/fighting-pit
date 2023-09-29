
from numpy import random

class Player:
    """Class representing both non-player characters and player-characters
    participating in the pit fights.
    """
    def __init__(self, rank:int, name:str, race:str, is_pc: bool) -> None:
        self.place = int(rank)
        self.player_name = name
        self.race = race
        self.is_pc = bool(is_pc)
        
    def generate_rolls(self) -> list: 
       return list(random.randint(1,21,3))

    def is_winner(self):
        self.place -= 1
    
    def is_loser(self):
        self.place += 1
    
    def save(self):
        return {"place": self.place, "player_name": self.player_name, "race": self.race, \
            "is_pc": self.is_pc}
    
    @classmethod
    def create_random_challenger(cls):
        return Player(999,"Mysterious Stranger", "Human", False)




    