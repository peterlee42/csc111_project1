"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed

def handle_input(command: str, valid_actions: list[str], menu_commands: set[str]) -> Optional[tuple[str, str] | str]:
    """If command is a menu command, return the command itself.
    If the command's action is valid, parse it and return a tuple of the command's action and target.
    If the command is not valid, return None.

    Preconditions:
    - command == command.lower().strip()
    """

    if command in menu_commands:
        return command

    for valid_action in valid_actions:
        # Account for a space in the action.
        if command.startswith(valid_action + ' '):
            target = command[len(valid_action) + 1:].strip()
            return valid_action, target

    return None


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - # TODO add descriptions of public instance attributes as needed (DONE)
        - current_location_id: the current location ID of the player in the game.
        - ongoing: a boolean representing whether the game is ongoing or not.
        - player: a Player object representing the player in the game.

    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
        - self.current_location_id in self._locations
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    player = Player
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

        # Player attribute
        self.player = Player(initial_location_id)

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        # Go through each element associated with the 'locations' key in the file
        for loc_data in data['locations']:
            location_obj = Location(loc_data['id'], loc_data['brief_description'], loc_data['long_description'],
                                    loc_data['available_directions'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above (DONE)
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['target_position'], item_data['target_points'])
            items.append(item_obj)
        # YOUR CODE BELOW

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        # YOUR CODE BELOW
        if loc_id is None:
            return self._locations[self.current_location_id]
        elif loc_id not in self._locations:
            raise ValueError("Invalid location ID")
        else:
            return self._locations[loc_id]

    def get_item(self, given_item_name: str) -> Item:
        """Retrieves item object by a given item name. If item object does not exist, do nothing."""
        for item_obj in self._items:
            if item_obj.name == given_item_name:
                return item_obj

    def undo(self, current_game_log: EventList) -> None:
        """Undo the last action taken by the player."""
        # Make current location id the id of the previous event. Remove the last event from the game log.
        if current_game_log.is_empty():
            print("No actions to undo.")
        elif current_game_log.first.next is None:
            print("No actions to undo")
        else:
            # comment wtvr happening here
            prev_event = current_game_log.last.prev

            prev_command = prev_event.next_command
            prev_location_id = prev_event.id_num
            prev_location = self.get_location(prev_event.id_num)

            current_game_log.last = prev_event

            current_game_log.last.next = None
            current_game_log.last.next_command = None

            if prev_command.startswith('pick up'):
                prev_item_name = prev_command[8:]
                self.player.drop_item(prev_location, prev_item_name)
            elif prev_command.startswith('drop'):
                prev_item_name = prev_command[5:]
                self.player.pick_up_item(prev_location, prev_item_name)
            elif prev_command.startswith('use'):
                prev_item_name = prev_command[4:]
                prev_item_obj = self.get_item(prev_item_name)
                self.player.undo_use(prev_location, prev_item_name, prev_item_obj)
            else:
                print('You have been move back to your previous location.')

            self.current_location_id = prev_location_id
            self.player.current_location = self._locations[prev_location_id]


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    # load data, setting initial location ID to 1
    game = AdventureGame('game_data.json', 1)
    # Regular menu options available at each location
    menu = {"look", "inventory", "score", "undo", "log", "quit"}
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location (DONE)
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE
        if choice not in menu:
            game_log.add_event(
                Event(location.id_num, location.brief_description), choice)

        # TODO: Depending on whether or not it's been visited before, (DONE)
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)
            location.visited = True

        # Display Location's Item Descriptions if there is any.
        for item in location.items:
            if game.get_item(item) is not None:
                print('- ', game.get_item(item).description)

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for direction in location.available_directions:
            print("- go", direction)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        handled_choice = handle_input(choice, game.player.available_actions, menu)
        while not handled_choice:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
            handled_choice = handle_input(choice, game.player.available_actions, menu)

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if choice == "log":
                game_log.display_events()
            elif choice == "quit":
                game.ongoing = False
            elif choice == "undo":
                game.undo(game_log)
            elif choice == "inventory":
                game.player.display_inventory()
            elif choice == "score":
                print("Score:", game.player.score)
            elif choice == "look":
                print(location.long_description)
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
        else:
            # In this case, you always have 2 parts. An action and a target.
            player_action, player_target = handled_choice

            # Change to new location
            if player_action == 'go':
                result = location.available_directions[player_target]
                game.current_location_id = result
            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            elif player_action == 'pick up':
                game.player.pick_up_item(location, player_target)
            elif player_action == 'use':
                game.player.use(game.current_location_id, player_target,
                                game.get_item(player_target))
            elif player_action == 'drop':
                game.player.drop_item(location, player_target)

        # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game

        print("========")
