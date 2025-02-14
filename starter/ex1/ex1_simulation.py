"""CSC111 Exercise 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Exercise 1 that allows a user to simulate the
playthrough of the game. Please consult the project handout for instructions and details.

The methods and classes in this file are all REQUIRED. You should complete them exactly
per the provided specification.

Do NOT modify any function/method headers, type contracts, etc. in this class (similar
to CSC110 assignments).

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

from ex1_event_logger import Event, EventList


# Note: We have completed the Location class for you. Do NOT modify it here, for ex1.
@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: integer id for this location
        - description: brief description of this location
        - available_commands: a mapping of available commands at this location to
                                the location executing that command would lead to
    """
    id_num: int
    description: str
    available_commands: dict[str, int]


class SimpleAdventureGame:
    """A simple text adventure game class storing all location data.

    Instance Attributes:
        - current_location_id: the ID of the location the game is currently in
    """

    # Private Instance Attributes:
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    _locations: dict[int, Location]
    current_location_id: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file.

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # Note: We have completed this method for you. Do NOT modify it here, for ex1.

        self._locations = self._load_game_data(game_data_file)
        self.current_location_id = initial_location_id  # game begins at this location

    @staticmethod
    def _load_game_data(filename: str) -> dict[int, Location]:
        """Load locations and items from a JSON file with the given filename and
        return a dictionary of locations mapping each game location's ID to a Location object."""

        # Note: We have completed this method for you. Do NOT modify it here, for ex1.

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['long_description'], loc_data['available_commands'])
            locations[loc_data['id']] = location_obj

        return locations

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        if loc_id is None:
            loc_id = self.current_location_id
        return self._locations[loc_id]


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: SimpleAdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._game = SimpleAdventureGame(game_data_file, initial_location_id)
        self._events = EventList()

        initial_location = self._game.get_location()
        self._events.add_event(Event(initial_location_id, initial_location.description))

        self.generate_events(commands, initial_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        for command in commands:
            self._game.current_location_id = current_location.available_commands[command]

            next_location = self._game.get_location()

            self._events.add_event(Event(next_location.id_num, next_location.description), command)
            current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east"])
        >>> sim.get_id_log()
        [1, 2]

        >>> sim = AdventureGameSimulation('sample_locations.json', 1, ["go east", "go east", "buy coffee"])
        >>> sim.get_id_log()
        [1, 2, 3, 3]
        """

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        return self._events.get_id_log()

    def run(self) -> None:
        """Run the game simulation and log location descriptions."""

        # Note: We have completed this method for you. Do NOT modify it for ex1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


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
