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
    visited: bool = False

    def __init__(self, location_id, brief_description, long_description, available_commands, items,
                 visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = location_id
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited

        # Initialize pick up commands
        for item in items:
            self.available_commands[f'pick up {item}'] = self.id_num


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here
        - name: the name of the item
        - start_position:
        - target_position:
        - target_points: points awarded when the item is placed at its correct location

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
        - name != ''
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
    start_position: int
    target_position: int
    target_points: int


class Player:
    """An item in our text adventure game world.

    Instance Attributes:
        - current_location_id: the id of the location the player is currently in
        - inventory: a list of items the player has
        - available_commands: a list of commands the player can use

    Representation Invariants:
        - current_location_id >= 0
    """

    current_location: Location
    inventory: list[str]
    available_commands: list[str]
    score: int

    def __init__(self, current_location) -> None:
        """Initialize a new player object.
        """
        self.current_location = current_location
        self.inventory = []
        self.available_commands = []
        self.score = 0

    def use(self, current_location: Location, item_name: str, item_obj: Item) -> None:
        """Use an item in the player's inventory.
        """
        if current_location.id_num == item_obj.target_position:
            self.score += item_obj.target_points
            print(f"{item_name} has been used")
            self.inventory.remove(item_name)
            self.available_commands.remove(f'use {item_name}')
            self.available_commands.remove(f'drop {item_name}')
        else:
            print(f"{item_name} cannot be used at this location")

    def undo_use(self, prev_location: Location, item_name: str, item_obj: Item) -> None:
        """Undo the effects of the item in the player's inventory."""
        if prev_location.id_num == item_obj.target_position:
            self.score -= item_obj.target_points
            self.inventory.append(item_name)
            self.available_commands.append(f'use {item_name}')
            self.available_commands.append(f'drop {item_name}')

    def drop_item(self, current_location: Location, item_name: str) -> None:
        """Remove an item from the player's inventory."""
        self.inventory.remove(item_name)
        current_location.items.append(item_name)
        current_location.available_commands[f'pick up {item_name}'] = \
            current_location.id_num
        self.available_commands.remove(f'drop {item_name}')
        self.available_commands.remove(f'use {item_name}')

        print(f"{item_name} has been removed from your inventory.")

    def pick_up_item(self, current_location: Location, item_name: str) -> None:
        """Add an item to the player's inventory."""

        self.inventory.append(item_name)  # add to inventory
        current_location.items.remove(item_name)  # remove item from location

        current_location.available_commands.pop(
            f'pick up {item_name}')  # remove command from location

        self.available_commands.append(f'drop {item_name}')
        self.available_commands.append(f'use {item_name}')

        print(f"{item_name} has been added to your inventory.")


class puzzle:
    def __init__():
        pass

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
