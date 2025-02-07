"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass

# My imports
from random import randrange
from typing import Optional
import json


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here
        - id_num: the unique identifier of the location
        - name: the name of the location
        - brief_description: a short description for quick rederence
        - long_description: a longer description of the location displayed upon entering
        - available_commands: a dictionary of commands available in the location
        - items: a list of items available in the location
        - visited: a boolean that indicates if the location has been visited

    Representation Invariants:
        - id_num >= 0
        - name != ''
        - brief_description != ''
        - long_description != ''
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.
    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool

    def __init__(self, location_id, brief_description, long_description, available_directions, items,
                 visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_directions = available_directions
        self.items = items
        self.visited = visited


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here
        - name: the name of the item
        - description: a description of the item
        - start_position:
        - target_position:
        - target_points: points awarded when the item is placed at its correct location

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
        - name != ''
        - description != ''
        - start_position >= 0
        - target_position >= 0
        - target_points >= 0
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    description: str
    start_position: int
    target_position: int
    target_points: int
    interactive: str


class Player:
    """An item in our text adventure game world.

    Instance Attributes:
        - current_location_id: the id of the location the player is currently in
        - inventory: a list of items the player has
        - available_commands: a list of actions that the player can use

    Representation Invariants:
        - current_location_id >= 0
    """

    current_location: Location
    inventory: list[str]
    available_actions: list[str]
    score: int
    messages: dict[str, list[str]]

    def __init__(self, current_location) -> None:
        """Initialize a new player object.
        """
        self.current_location = current_location
        self.inventory = []
        self.available_actions = ['go', 'pick up', 'use', 'drop']
        self.score = 0
        self.messages = self._load_game_data('player_messages.json')

    def get_random_message(self, message_type: str, item_name: Optional[str] = None) -> str:
        """Get a random message from the messages attribute based on the message type.
        If the type does not exist, do nothing."""
        article = ''

        if message_type in self.messages:
            random_index = randrange(len(self.messages[message_type]))
            random_message = self.messages[message_type][random_index]

            if item_name is None or '{item}' not in random_message:
                return self.messages[message_type][random_index].capitalize()
            else:
                return self.messages[message_type][random_index].format(item=f'{item_name}').capitalize()

    def use(self, current_location_id_num: int, item_name: str, item_obj: Item) -> None:
        """Use an item in the player's inventory.
        """
        if item_name in self.inventory:
            if current_location_id_num == item_obj.target_position:
                self.score += item_obj.target_points
                self.inventory.remove(item_name)
                print(self.get_random_message('item_used', item_name))
                Interactive.interact(self, item_name, item_obj)
            else:
                print(self.get_random_message('item_cannot_be_used', item_name))
        else:
            print(self.get_random_message('item_does_not_exist', item_name))

    @staticmethod
    def _load_game_data(filename: str) -> dict[str, list[str]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        player_messages = {}
        # Go through each element associated with the 'message_types' key in the file
        # Map each type of message to the list of all messages of that type.
        for message_type in data['message_types']:
            player_messages[message_type['type']] = message_type['messages']

        return player_messages

    def undo_use(self, prev_location: Location, item_name: str, item_obj: Item) -> None:
        """Undo the effects of the item in the player's inventory."""
        if prev_location.id_num == item_obj.target_position:
            self.score -= item_obj.target_points
            self.inventory.append(item_name)

    def drop_item(self, current_location: Location, item_name: str) -> None:
        """Remove an item from the player's inventory."""
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            current_location.items.append(item_name)

            print(self.get_random_message('item_removed_from_inventory', item_name))
        else:
            print(self.get_random_message('item_does_not_exist', item_name))

    def pick_up_item(self, current_location: Location, item_name: str) -> None:
        """Add an item to the player's inventory. Reward the player with 1 point."""
        if item_name in current_location.items:

            self.inventory.append(item_name)  # add to inventory
            current_location.items.remove(item_name)  # remove item from location

            # add 1 point to score for picking up item
            self.score += 1

            print(self.get_random_message('item_picked_up', item_name))
        else:
            print(self.get_random_message('item_does_not_exist', item_name))

    def display_inventory(self) -> None:
        """Displays the player's current inventory"""
        if not self.inventory:
            print(self.get_random_message('inventory_empty'))
        else:
            print(self.get_random_message('currently_have'))
            for item in self.inventory:
                print('- ', item)


class Interactive:
    """
    Objects that a player can interact with within the game.
    """

    @staticmethod
    def interact(player: Player, item_name: str, item_obj: Item) -> None:
        """Interact with an item using the interactive object.

        This method dynamically retrieves and calls the method specified by
        the string in `item_obj.interactive`. For example, if
        `item_obj.interactive` is "vending_machine", then this method will
        effectively call `Interactive.vending_machine(item_name, player)`.
        """
        method_name = getattr(item_obj, 'interactive', None)
        if not method_name:
            print("")
            return

        # Dynamically get the corresponding method from the Interactive class
        method = getattr(Interactive, method_name, None)
        if callable(method):
            method(item_name, player)
        else:
            print("a")

    @staticmethod
    def vending(item_name: str, player: Player) -> None:
        """Simulate a vending machine interaction when using a toonie."""

        player.inventory.append("energy drink")
        print("You insert your toonie into the vending machine. It whirs for a moment and dispenses an energy drink into your inventory.")






# class puzzle:
#     def __init__():
#         pass

# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

