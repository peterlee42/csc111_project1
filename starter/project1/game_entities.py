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
        - id_num: the unique identifier of the location
        - name: the name of the location
        - brief_description: a short description for quick rederence
        - long_description: a longer description of the location displayed upon entering
        - available_directions: a dictionary of available directions in the location
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
    available_directions: dict[str, int]
    items: list[str]
    visited: bool
    acquired_items: list[str]

    def __init__(self, location_id, name, brief_description, long_description, available_directions, items,
                 acquired_items, visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = location_id
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_directions = available_directions
        self.items = items
        self.acquired_items = acquired_items
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


class Player:
    """A player in our text adventure game world.

    Instance Attributes:
        - inventory: a list of items the player has
        - available_commands: a list of actions that the player can use

    Representation Invariants:
        - current_location_id >= 0
    """
    inventory: list[str]
    available_actions: list[str]
    score: int
    messages: dict[str, list[[str]]]

    def __init__(self, current_location) -> None:
        """Initialize a new player object.
        """
        self.inventory = []
        """TODO : I want to add consume, give, and interact (maybe npc class)..."""
        self.available_actions = ['go', 'pick up', 'use', 'drop']
        self.score = 0
        self.messages = self._load_player_messages('player_messages.json')

    def _get_random_message(self, message_type: str, item_name: Optional[str] = None) -> str:
        """Get a random message from the messages attribute based on the message type.
        If the type does not exist, do nothing."""
        if message_type in self.messages:
            random_index = randrange(len(self.messages[message_type]))
            random_message = self.messages[message_type][random_index]

            if item_name is None or '{item}' not in random_message:
                return random_message
            else:
                formatted_message = random_message.format(item=item_name)
                return formatted_message[0].upper() + formatted_message[1:]

    @staticmethod
    def _load_player_messages(filename: str) -> dict[str, list[str]]:
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

    def use(self, current_location: Location, item_obj: Optional[Item]) -> None:
        """Use an item in the player's inventory."""
        if not item_obj or item_obj.name.lower() not in self.inventory:
            print(self._get_random_message('item_does_not_exist', item_obj.name))
        elif current_location.id_num == item_obj.target_position:
            item_name = item_obj.name.lower()
            print(self._get_random_message('item_used', item_name))
            random_index = randrange(len(current_location.acquired_items))
            acquired_item = current_location.acquired_items[random_index]
            self.score += item_obj.target_points
            self.inventory.remove(item_name)
            self.inventory.append(acquired_item.lower())
            print(f'You received: {acquired_item}')
        else:
            print(self._get_random_message('item_cannot_be_used', item_obj.name))

    def undo_use(self, prev_location: Location, item_obj: Item) -> None:
        """Undo the effects of the item in the player's inventory."""
        item_name = item_obj.name.lower()
        if prev_location.id_num == item_obj.target_position:
            self.score -= item_obj.target_points
            self.inventory.pop()
            # if acquired_item not in prev_location.acquired_items:
            #     prev_location.acquired_items.append(acquired_item)
            self.inventory.append(item_name)
            print("The effect of your item has been undone.")

    def drop_item(self, current_location: Location, item_name: str) -> None:
        """Remove an item from the player's inventory."""
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            current_location.items.append(item_name)

            print(self._get_random_message('item_removed_from_inventory', item_name))
        else:
            print(self._get_random_message('item_does_not_exist', item_name))

    def go(self, current_location: Location, direction: str):
        """Return the id of the new location if the direction is valid. Return the current location id otherwise.

        Representation Invariants:
        - direction == direction.lower().split()
        """
        if direction in current_location.available_directions:
            return current_location.available_directions[direction]
        else:
            print("Looks like that isn't a valid direction...")
            return current_location.id_num

    def pick_up_item(self, current_location: Location, item_name: str) -> None:
        """Add an item to the player's inventory. Reward the player with 1 point.
        Representation Invariants:
        - item_name == item_name.lower().split()
        """
        if item_name in current_location.items:

            self.inventory.append(item_name)  # add to inventory
            current_location.items.remove(item_name)  # remove item from location

            # add 1 point to score for picking up item
            self.score += 1

            print(self._get_random_message('item_picked_up', item_name))
        else:
            print(self._get_random_message('item_does_not_exist', item_name))

    def display_inventory(self) -> None:
        """Displays the player's current inventory"""
        if not self.inventory:
            print(self._get_random_message('inventory_empty'))
        else:
            print(self._get_random_message('currently_have'))
            for item in self.inventory:
                print('- ', item)


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
