import json


# initialize food items from the menu
class Menu:
    def __init__(self):
        self.foods = []

    # get food from the menu
    def get_foods(self):
        with open('dinning_hall_data/menu.json') as json_file:
            self.foods = json.load(json_file)
        return self.foods
