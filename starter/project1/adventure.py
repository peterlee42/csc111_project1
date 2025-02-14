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
from dataclasses import dataclass
from typing import Optional

# My imports
from datetime import time

from game_entities import Location, Item, Player, Npc, LocationEntities
from proj1_event_logger import Event, EventList


def parse_command(command: str, valid_actions: list[str]) -> tuple[str, str]:
    """If the command's action is valid, parse it and return a tuple of the command's action and target.
    Otherwise, return a tuple of the original command and an empty string.

    Preconditions:
    - command != ''
    """
    for valid_action in valid_actions:
        # Account for a space in the action.
        if command.startswith(valid_action + ' '):
            target = command[len(valid_action) + 1:].strip()
            return valid_action, target

    return command, ''


@dataclass
class TimeWindow:
    """A dataclass representing the current time and the deadline time

    Instance Attributes:
        - current_time: The current time of this time window
        - deadline: The deadline of this time window
    """
    current_time: time
    deadline: time


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - ongoing: a boolean representing whether the game is ongoing or not.
        - player: a Player object representing the player in the game.
        - time_window: A TimeWindow object representing the current time and deadline in the game.

    Representation Invariants:
        - self.current_location_id in self._locations
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.
    #   - _npcs: a list of Npc objects, reprsenting all none playable characters in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    _npcs: list[Npc]
    current_location_id: int
    player: Player
    time_window: TimeWindow
    ongoing: bool

    def __init__(self, game_data_file: str, initial_location_id: int,
                 time_window: TimeWindow) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        - start_time < end_time
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Game data
        self._locations, self._items, self._npcs = self._load_game_data(game_data_file)

        self.current_location_id = initial_location_id

        # Player attribute
        self.player = Player()

        # Game start time and deadline time.
        self.time_window = time_window

        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item], list[Npc]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        # Go through each element associated with the 'locations' key in the file
        for loc_data in data['locations']:
            location_obj_entities = LocationEntities(loc_data['items'], loc_data['given_items'], loc_data['npcs'])
            location_obj = Location(loc_data['id'], loc_data['name'], (loc_data['brief_description'],
                                                                       loc_data['long_description']),
                                    loc_data['available_directions'],
                                    location_obj_entities)
            locations[loc_data['id']] = location_obj

        items = []

        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'],
                            item_data['start_position'], item_data['target_position'], item_data['target_points'])
            items.append(item_obj)

        npcs = []
        for npc_data in data['npcs']:
            npc_obj = Npc(npc_data['name'], npc_data['dialogue'], npc_data['location_id'],
                          (npc_data['quest_message'], npc_data['quest_complete_message']),
                          npc_data['required_items'], npc_data['reward'])
            npcs.append(npc_obj)

        return locations, items, npcs

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the player's current location.
        """
        # YOUR CODE BELOW
        if loc_id is None:
            return self._locations[self.current_location_id]
        elif loc_id not in self._locations:
            raise ValueError("Invalid location ID")
        else:
            return self._locations[loc_id]

    def get_item(self, item_name: str) -> Optional[Item]:
        """Retrieves item object by a given item name. If item object does not exist, return None.
        """
        for item_obj in self._items:
            if item_name.lower() == item_obj.name.lower():
                return item_obj

        return None

    def get_npc(self, npc_name: str) -> Optional[Npc]:
        """Retrieves npc object by a given npc name. If npc object does not exist, return None.

        Preconditions:
        - npc_name == npc_name.strip()
        """
        for npc_obj in self._npcs:
            if npc_name.lower() == npc_obj.name.lower():
                return npc_obj

        return None

    def undo(self, current_game_log: EventList) -> None:
        """Undo the last action taken by the player."""
        # Check if there are actions to undo
        if current_game_log.is_empty() or current_game_log.first.next is None:
            print("No actions to undo.")
            return

        prev_event = current_game_log.last.prev

        # Change current time to the time of the previous action
        self.time_window.current_time = prev_event.event_time

        # changes current location id to the previous one
        self.current_location_id = prev_event.id_num
        prev_location = self.get_location()

        # Retrieve the previous command and since we know it already exists, we don't have to check anything.
        prev_command = prev_event.next_command
        prev_action, prev_target = parse_command(
            prev_command, self.player.available_actions)

        if prev_action == 'pick up':
            prev_item_obj = self.get_item(prev_target)
            self.player.inventory.remove(prev_item_obj.name)
            prev_location.location_entities.items.append(prev_item_obj.name)
        elif prev_action == 'drop':
            prev_item_obj = self.get_item(prev_target)
            self.player.inventory.append(prev_item_obj.name)
            prev_location.location_entities.items.remove(prev_item_obj.name)
        elif prev_action == 'use':
            prev_item_obj = self.get_item(prev_target)

            self.player.score -= prev_item_obj.target_points

            for given_item in prev_location.location_entities.given_items:
                self.player.inventory.remove(given_item)  # remove any given items

            # add previous target item
            self.player.inventory.append(prev_target)

        elif prev_action == 'interact':
            prev_npc = self.get_npc(prev_target)
            self.player.undo_interaction(prev_npc)

        print('Action undone!')

        current_game_log.remove_last_event()

    def add_minutes(self, added_minutes: int) -> bool:
        """Adds minutes to self.current_time.
        Returns return true if the player passed the deadline. Return False otherwise.

        Preconditions:
        - 0 <= added_minutes <= 60
        """
        current_hour, current_minute = self.time_window.current_time.hour, self.time_window.current_time.minute
        current_minute += added_minutes
        current_hour += current_minute // 60
        current_minute %= 60

        day_passed = False
        if current_hour >= 24:
            current_hour %= 24
            day_passed = True

        new_time = time(hour=current_hour, minute=current_minute)
        self.time_window.current_time = new_time

        if day_passed or self.time_window.current_time >= self.time_window.deadline:
            return True
        return False

    def check_win(self, initial_location_id: int, deadline_passed: bool, win_items: list[str]) -> None:
        """Checks if the player has won. If the time has passed the deadline, the player has lost.
        If player has brought all win items in the initial location before the deadline, they have
        won.
        """
        if deadline_passed:
            print('========')
            print('YOU MISSED THE DEADLINE!\n')
            print('Current Time:', self.time_window.current_time.strftime("%I:%M %p"))
            print('Your Final Score:', self.player.score)
            self.ongoing = False

        elif self.current_location_id == initial_location_id and all({item in self.player.inventory
                                                                      for item in win_items}):
            # Case where player is back at original location AND has all win items in their inventory.
            total_score = sum([self.get_item(item).target_points for item in win_items])
            self.player.score += total_score
            self.ongoing = False
            print('========')
            print('You submitted on before the deadline! Congratulations!\n')
            print('Time of submission:', self.time_window.current_time)
            print('Your Final Score:', self.player.score)

    def display_location_info(self, location: Location) -> None:
        """Display information about the given location in the console. This include the location description, items,
        and npcs.
        """
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        if location.visited:
            print(location.descriptions[0])
        else:
            print(location.descriptions[1])
            location.visited = True

        # Display Location's Item Name if there is any.
        if location.location_entities.items:
            print("At this location, you can pick up:")
            for location_item in location.location_entities.items:
                print(f'- {location_item}')

        # Display interactive NPCs if there is any.
        if location.location_entities.npcs:
            print("At this location, you can interact with:")
            for location_npc in location.location_entities.npcs:
                print(f'- {location_npc}')


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_initial_location_id = 1
    game_win_items = ['laptop', 'laptop charger', 'lucky UofT mug', 'USB drive']

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    # load data, setting initial location ID to 1, start_time to 8:00 AM, and deadline to 4:00 PM
    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
    game = AdventureGame('game_data.json', game_initial_location_id,
                         game_time_window)
    # Regular menu options available at each location
    menu = ["look", "inventory", "score", "undo", "log", "quit", "quests"]
    choice = None
    valid_move = True
    action_time = 0

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        current_location = game.get_location()

        # Add event to game_log if it is a valid, non menu, move.
        if choice not in menu and valid_move:
            game_log.add_event(
                Event(current_location.id_num, current_location.descriptions[0], game.time_window.current_time), choice)

        # display location info
        game.display_location_info(current_location)

        # Display the current time
        print(f"\nThe current time is {game.time_window.current_time.strftime("%I:%M %p")}.")

        # Display menu actions
        print("What to do? Choose from: look, quests, inventory, score, undo, log, quit")

        # Display directions the player can go
        print("At this location, you can go:")
        for direction in current_location.available_directions:
            print('-', direction)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        player_action, player_target = parse_command(choice, game.player.available_actions)
        while player_action not in game.player.available_actions and player_action not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()
            player_action, player_target = parse_command(choice, game.player.available_actions)

        print("========")
        print(f"You decided to: {player_action} {player_target}")

        if player_action in menu:
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            if player_action == "log":
                game_log.display_events()
            elif player_action == "quit":
                print('Bye bye!')
                game.ongoing = False
            elif player_action == "undo":
                game.undo(game_log)
            elif player_action == "inventory":
                game.player.display_inventory()
            elif player_action == "score":
                print("Score:", game.player.score)
            elif player_action == "look":
                print(current_location.descriptions[1])
            elif player_action == "quests":
                game.player.display_quests()
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)
        else:
            if player_action == 'go':
                result = game.player.go(current_location, player_target)

                # add to time if it is a new location
                if game.current_location_id != result:
                    action_time = 10
                    valid_move = True
                else:
                    valid_move = False
                # Change to new location (or the same)
                game.current_location_id = result
            elif player_action == 'pick up':
                valid_move = game.player.pick_up_item(current_location, player_target)
                action_time = 2
            elif player_action == 'use':
                player_target_obj = game.get_item(player_target)
                valid_move = game.player.use(current_location, player_target_obj)
                action_time = 3
            elif player_action == 'drop':
                valid_move = game.player.drop_item(current_location, player_target)
                action_time = 2
            elif player_action == 'examine':
                player_target_obj = game.get_item(player_target)
                valid_move = game.player.examine_item(player_target_obj)
                action_time = 2
            elif player_action == 'interact':
                target_npc_obj = game.get_npc(player_target)
                rewarded_points = sum([game.get_item(item).target_points for item in target_npc_obj.required_items
                                       if target_npc_obj])
                valid_move = game.player.interact(game.current_location_id, target_npc_obj, rewarded_points)
                action_time = 5

            # If it's a valid move, then add minutes and check if time has passed the deadline.
            player_lost = False
            if valid_move:
                player_lost = game.add_minutes(action_time)
            # Checks if the player has won
            game.check_win(game_initial_location_id, player_lost, game_win_items)

        print("========")
