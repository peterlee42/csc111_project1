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

from scipy.constants import minute

from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList

from datetime import time


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed

def parse_command(command: str, valid_actions: list[str]) -> Optional[tuple[str, str]]:
    """If command is a menu command, return the command itself.
    If the command's action is valid, parse it and return a tuple of the command's action and target.
    If the command is not valid, return None.

    Preconditions:
    - command == command.lower().strip()
    """
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
        - ongoing: a boolean representing whether the game is ongoing or not.
        - player: a Player object representing the player in the game.
        - current_time: the current time in the game (24 hour time)
        - deadline: the deadline of the assignment (24 hour time)

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
    ongoing: bool  # Suggested attribute, can be removed
    current_time: time
    deadline: time
    """- # TODO total_moves"""

    def __init__(self, game_data_file: str, initial_location_id: int, start_time: tuple[int, int],
                 deadline: tuple[int, int]) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        - 0 <= start_time[0] <= 23
        - 0 <= deadline[0] <= 23
        - 0 <= start_time[1] <= 59
        - 0 <= deadline[1] <= 59
        - (start_time[0] < deadline[0] or (start_time[0] == deadline[0] and start_time[1] < deadline[1]))
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
        self.player = Player()

        self.current_time = time(hour=start_time[0], minute=start_time[1])
        self.deadline = time(hour=deadline[0], minute=deadline[1])

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
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'], loc_data['available_directions'],
                                    loc_data['items'], loc_data['acquired_items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above (DONE)
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['full_name'], item_data['description'],
                            item_data['start_position'], item_data['target_position'], item_data['target_points'],
                            item_data['item_type'])
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

    def get_item(self, item_name: str) -> Item | None:
        """Retrieves item object by a given item name. If item object does not exist, return None.

        Preconditions:
        - item_name == item_name.lower.strip()
        """
        for item_obj in self._items:
            if item_obj.name.lower().strip() == item_name:
                return item_obj
        return None

    def undo(self, current_game_log: EventList) -> None:
        """Undo the last action taken by the player."""
        # Make current location id the id of the previous event. Remove the last event from the game log.
        if current_game_log.is_empty() or current_game_log.first.next is None:
            print("No actions to undo.")
        else:
            # Undo the game log
            prev_event = current_game_log.last.prev

            prev_location_id = prev_event.id_num
            prev_location = self.get_location(prev_location_id)

            current_game_log.last = prev_event

            # Retrieve the previous command
            prev_command = prev_event.next_command
            prev_action, prev_target = parse_command(
                prev_command, self.player.available_actions)

            if prev_action == 'pick up':
                self.player.inventory.remove(prev_target)
                prev_location.items.append(prev_target)
            elif prev_action == 'drop':
                self.player.inventory.remove(prev_target)
                prev_location.items.append(prev_target)
            elif prev_action == 'use':
                prev_item_obj = self.get_item(prev_target)

                self.player.score -= prev_item_obj.target_points
                self.player.inventory.pop()  # remove any acquired items
                self.player.inventory.append(prev_target)  # add previous target item
            else:
                self.current_location_id = prev_location_id

            print('Action undone!')

            # Remove the most recent command
            current_game_log.last.next = None
            current_game_log.last.next_command = None

    def add_minutes(self, added_minutes: int) -> None:
        """Adds specified minutes to self.current_time

        Preconditions:
        - 0 <= added_minutes <= 60
        """
        current_hour = self.current_time.hour
        current_minute = self.current_time.minute

        current_minute += added_minutes

        current_hour += current_minute // 60
        current_minute %= 60

        # If you add to many hours such that it goes to the next day, automatically stop the game.
        if current_hour // 24 == 0:
            self.current_time = time(current_hour, current_minute)
        else:
            current_hour %= 24
            print(f'It is {time(hour=current_hour, minute=current_minute)} the next day!')
            print('YOU MISSED THE DEADLINE! YOU FAILED!')
            self.ongoing = False

    def check_lose(self) -> None:
        """Check if the deadline has passed"""
        if self.current_time >= self.deadline:
            print('YOU MISSED THE DEADLINE! YOU FAILED!')
            self.ongoing = False


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
    game = AdventureGame('game_data.json', 1, (8, 0), (9, 30))
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
            print(location.long_description)  # TODO: this looks ugly
            location.visited = True

        # Display Location's Item Name if there is any.
        for item in location.items:
            if game.get_item(item):
                print(f'- There is {game.get_item(item).full_name}')

        # display the current time
        print(f"\nThe current time is {game.current_time}.")
        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can go:")
        for direction in location.available_directions:
            print('-', direction.title())  # TODO: capitalize or title???

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        parsed_choice = parse_command(choice, game.player.available_actions)
        while not parsed_choice and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
            parsed_choice = parse_command(
                choice, game.player.available_actions)

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
            player_action, player_target = parsed_choice
            player_target_obj = game.get_item(player_target)  # TODO: Maybe handle this better

            # Change to new location
            if player_action == 'go':
                result = game.player.go(location, player_target)

                if game.current_location_id != result:
                    game.add_minutes(10)

                game.current_location_id = result
            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            elif player_action == 'pick up' and game.player.pick_up_item(location, player_target):
                game.add_minutes(2)
            elif player_action == 'use' and game.player.use(location, player_target_obj):
                game.add_minutes(2)
            elif player_action == 'drop' and game.player.drop_item(location, player_target):
                game.add_minutes(2)
            elif player_action == 'examine' and game.player.examine_item(player_target_obj):
                game.add_minutes(1)

        # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game

        print("========")

        game.check_lose()
