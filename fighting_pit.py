from player import Player
import pandas as pd
from numpy import random
from fight import AutomaticFight
import sys



class FightingPit:
    """This class simulates fights in a fighting pit.
    """
    def __init__(self, name:str, number_of_fights:int) -> None:
        self.name = name
        self.fight = None # place holder for the current fight in the pit
        self.number_of_fights = number_of_fights
        self.records_file = ""
        
    def load_players(self):
        """Method reads in the existing csv file with the rankings
        for the current pit and creates a Player object for each row in the
        dataframe, representing a player ready to fight.
        """
        self.fighters = []
        try:
            self.records_file = pd.read_csv(self.name+".csv")
        except FileNotFoundError:
            print(f"No fighting pit under the name '{self.name}' found. "+\
                "Give another name or create a new pit.")
        else:
            for index, row in self.records_file.iterrows():
                player = Player(row.place, row.player_name, row.race, row.is_pc)
                self.fighters.append(player)
    
    def find_fighters(self):
        try_count = 0
        while try_count < 10:
            challenger_index = random.randint(1, len(self.fighters))
            defender_index = challenger_index - 1
            try:
                self.fight = AutomaticFight(challenger = self.fighters[challenger_index], \
                    defender = self.fighters[defender_index])
                self.fight.fight_commentary()
                self.save_current_rankings()
                break
            except ValueError:
                try_count += 1
  
    def save_current_rankings(self):
        """This method calls the save() method on every player object
        and gathers the results into a rankings dictionary,
        which is later sorted and saved as a new csv.
        """
        rankings = {"place" : [], "player_name": [], "race": [], "is_pc": []}
        for player in self.fighters:
            player_info = player.save()
            for key, value in player_info.items():
                rankings[key].append(value)

        rankings_df = pd.DataFrame(rankings).sort_values(by="place",\
            ascending=True) # saving it in a df form with sorted values
        self.records_file = rankings_df
        rankings_df.to_csv(self.name+".csv", index = False)

    def display_current_rankings(self):
        if len(self.records_file) > 1:
            print(self.records_file)

    def run(self):
        for x in range(self.number_of_fights):
            try:
                self.load_players()
                self.find_fighters()
            except ValueError as e:
                print(e)
                break

        self.display_current_rankings()
            

if __name__ == "__main__":
    try:
        # for reading in atributes directly from the command line
        name = sys.argv[1]
        number_of_fights = sys.argv[2]
    except IndexError:
        name = input("Type the name of the fighting pit: ")
        number_of_fights = input("How many fights do you want to simulate? ")
    
    pit = FightingPit(name = name, number_of_fights=int(number_of_fights))
    pit.run()

        
# IDEAS FOR FUTURE DEVELOPMENT
#TODO: create a mode for simulating weeks of being absent from the fighting pit
# This involves the mechanic that if a PC is challenged to a fight, it's an automatic loss.
# Pass in number of weeks instead of number of fights. 5-ish fights per week?

#TODO: create a PitFactory with a feature to create random NPCs

#TODO: Create a mechanic with a small chance of a Mysterious Stranger entering the ring.