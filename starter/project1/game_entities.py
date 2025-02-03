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
import random
from dataclasses import dataclass
from pyexpat.errors import messages
from random import randrange


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

    def __init__(self, location_id, brief_description, long_description, available_commands, items,
                 visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        For each item in the location, initialize a pick up command.
        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
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
    messages: dict[str, list[[str]]]

    def __init__(self, current_location) -> None:
        """Initialize a new player object.
        """
        self.current_location = current_location
        self.inventory = []
        self.available_actions = ['go', 'pick up', 'use', 'drop']
        self.score = 0
        self.messages = {
            "item_used": [
                "{item_name} has been used.",
                "You successfully used {item_name}.",
                "{item_name} works as intended.",
                "{item_name} is now in action!",
                "You use {item_name} with precision."
            ],
            "item_cannot_be_used": [
                "{item_name} cannot be used at this location.",
                "Using {item_name} here has no effect.",
                "{item_name} doesn't seem to work in this place.",
                "Nothing happens when you try to use {item_name} here.",
                "{item_name} isn't useful in this situation."
            ],
            "item_does_not_exist": [
                "{item_name}? That doesn't seem to exist.",
                "You can't find any trace of {item_name}.",
                "{item_name} isn’t part of this world… or is it?",
                "There’s no such thing as {item_name} here.",
                "{item_name} sounds unfamiliar—are you sure it exists?",
                "Your mind conjures {item_name}, but reality disagrees."
                "Hmmm... Maybe look somewhere else.",
                "You reach out, but grasp only empty air.",
                "You search thoroughly but find nothing of the sort.",
                "Nothing like that is around here.",
                "Your search yields nothing. Perhaps it’s hidden elsewhere.",
                "The item eludes you, as if it was never here to begin with."
            ],
            "item_picked_up": [
                "{item_name} has been added to your inventory.",
                "You have picked up {item_name}.",
                "Nice! {item_name} is in your inventory.",
                "{item_name} is now safely in your possession.",
                "You carefully stow {item_name} into your inventory.",
                "Success! {item_name} is now yours."
            ],
            "item_removed_from_inventory": [
                "{item_name} has been removed from your inventory.",
                "You dropped {item_name}.",
                "{item_name} is no longer in your possession.",
                "You carefully set down {item_name}.",
                "You let go of {item_name}, leaving it behind."
            ],
            "inventory_empty": [
                "Your inventory is empty!",
                "You’re not carrying anything right now.",
                "Nothing in your inventory at the moment.",
                "Your pockets are completely empty."
            ],
            "currently_have": [
                "You currently have:",
                "You're carrying the following items:",
                "Your inventory contains:"
            ]
        }

    # random message generator based on type of message
    def get_random_message(self, message_type: str) -> str:
        """Get a random message from the messages attribute based on the message type.
        If the type does not exist, do nothing."""
        if message_type in self.messages:
            random_index = randrange(len(self.messages[message_type]))
            return self.messages[message_type][random_index]

    def use(self, current_location_id_num: int, item_name: str, item_obj: Item) -> None:
        """Use an item in the player's inventory.
        """
        if item_name in self.inventory:
            if current_location_id_num == item_obj.target_position:
                self.score += item_obj.target_points
                self.inventory.remove(item_name)

                print(self.get_random_message('item_used').format(item_name=item_name))
            else:
                print(self.get_random_message('item_cannot_be_used').format(item_name=item_name))
        else:
            print(self.get_random_message('item_does_not_exist').format(item_name=item_name))

    def undo_use(self, prev_location: Location, item_name: str, item_obj: Item) -> None:
        """Undo the effects of the item in the player's inventory."""
        if prev_location.id_num == item_obj.target_position:
            self.score -= item_obj.target_points
            self.inventory.append(item_name)

    def drop_item(self, current_location: Location, item_name: str) -> None:
        """Remove an item from the player's inventory."""
        self.inventory.remove(item_name)
        current_location.items.append(item_name)

        print(self.get_random_message('item_removed_from_inventory'))

    def pick_up_item(self, current_location: Location, item_name: str) -> None:
        """Add an item to the player's inventory. Reward the player with 1 point."""
        if item_name in current_location.items:

            self.inventory.append(item_name)  # add to inventory
            current_location.items.remove(item_name)  # remove item from location

            # add 1 point to score for picking up item
            self.score += 1
            print(self.get_random_message('item_picked_up').format(item_name=item_name))
        else:
            print(self.get_random_message('item_does_not_exist').format(item_name=item_name))

    def display_inventory(self) -> None:
        """Displays the player's current inventory"""
        if not self.inventory:
            print(self.get_random_message('inventory_empty'))
        else:
            print(self.get_random_message('currently_have'))
            for item in self.inventory:
                print('- ', item)


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
