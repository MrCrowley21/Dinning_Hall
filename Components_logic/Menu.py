import json

from config import *


# initialize food items from the menu
class Menu:
    def __init__(self):
        self.foods = []

    # get food from the menu
    def get_foods(self):
        with open(menu) as json_file:
            self.foods = json.load(json_file)
        return self.foods
