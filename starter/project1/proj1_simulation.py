"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate an entire
playthrough of the game. Please consult the project handout for instructions and details.

You can copy/paste your code from the ex1_simulation file into this one, and modify it as needed
to work with your game.

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
from datetime import time
from proj1_event_logger import Event, EventList
from adventure import AdventureGame, TimeWindow, parse_command
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, time_window: TimeWindow, commands: list[str]) \
            -> None:
        """Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id, time_window)

        start_location = self._game.get_location()
        start_time = time_window.current_time
        self._events.add_event(Event(initial_location_id, start_location.descriptions[0], start_time))

        # Hint: Call self.generate_events with the appropriate arguments
        self.generate_events(commands, start_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """Generate all events in this simulation.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands at each associated location in the game
        """

        # Hint: current_location.available_commands[command] will return the next location ID
        # which executing <command> while in <current_location_id> leads to

        menu = {"look", "inventory", "score", "undo", "log", "quit", "quests"}
        action_times = {"go": 10, "pick up": 2, "use": 3, "drop": 2, "examine": 2, "interact": 5}

        for command in commands:
            command = command.lower().strip()

            player_action, player_target = parse_command(command, self._game.player.available_actions)

            if player_action not in menu:
                if player_action == 'go':
                    # update the game's location id
                    result = self._game.player.go(current_location, player_target)
                    self._game.current_location_id = result

                # update game's current time
                self._game.add_minutes(action_times[player_action])

                next_location = self._game.get_location()

                self._events.add_event(Event(next_location.id_num, next_location.descriptions[0],
                                             self._game.time_window.current_time), command)
                current_location = next_location

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
        >>> sim = AdventureGameSimulation('game_data.json', 1, sim_time_window, ["go to lobby", "go outside", "go south", 'go inside McLennan', 'pick up pocoyo'])
        >>> sim.get_id_log()
        [1, 2, 3, 4, 13, 13]

        >>> sim_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
        >>> sim = AdventureGameSimulation('game_data.json', 1, sim_time_window, ["pick up tOOnie", "score", "go to lobby", "use toonie", "score","go to dorm"])
        >>> sim.get_id_log()
        [1, 1, 2, 2, 1]
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
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })

    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))

    # Create a list of all the commands needed to walk through your game to win it
    win_walkthrough = ["pick up toonie", "pick up five dollar bill", "go to lobby", "use toonie", "go outside",
                       "go south", "go inside McLennan", "pick up Pocoyo", "go to east exit",
                       "go to food trucks", "use five dollar bill", "go back", "go south",
                       "go inside Bahen", "go to CSSU lounge",
                       "interact Prof Sadia", "go to lobby", "go to east exit",
                       "go east", "go north", "go north", "go north", "go north", "go inside Myhal Centre",
                       "pick up student ID", "pick up backpack", "go outside myhal centre", "go south",
                       "go inside New College",
                       "interact Alex Carter", "go west exit", "go south", "go south", "go south", "go east",
                       "go south", "go west", "go inside Gerstein", "interact Security Guard", "go outside", "go east",
                       "go north", "go west", "go north", "go north", "go north", "go north", "go east",
                       "go inside Robarts", "pick up barista notes", "go to Robarts Commons", "interact tired student",
                       "go to robarts cafe",
                       "interact Barista", "go downstairs", "go to lobby", "go outside", "go west", "go south",
                       "go south", "go inside Sidney Smith", "use admin pass", "go outside", "go north", "go north",
                       "go west", "go west", "go inside Chestnut", "go to dorm"]

    # Win simulation
    expected_log = [1, 1, 1, 2, 2, 3, 4, 13, 13, 4, 6, 6, 4, 7, 8, 9, 9, 8, 12, 14, 16, 23, 25, 29, 30, 30, 30, 29, 25,
                    27, 27, 25, 23, 16, 14, 15, 17, 18, 20, 20, 18, 17, 15, 14, 16, 23, 25, 29, 31, 32, 32, 33, 33, 34,
                    34, 33, 32, 31, 29, 25, 23, 24, 24, 23, 25, 29, 28, 3, 2, 1]
    win_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, win_walkthrough)
    assert expected_log == win_sim.get_id_log()

    # Lose Simulation
    lose_demo = ["go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm"]
    expected_log = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    lose_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, lose_demo)
    assert expected_log == lose_sim.get_id_log()

    # Inventory demo
    inventory_demo = ["pick up toonie", "inventory", "go to lobby", "use toonie", "inventory"]
    expected_log = [1, 1, 2, 2]
    inventory_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, inventory_demo)
    assert expected_log == inventory_sim.get_id_log()

    # Scores demo
    scores_demo = ["pick up toonie", "score", "go to lobby", "use toonie", "score"]
    expected_log = [1, 1, 2, 2]
    scores_sim = AdventureGameSimulation('game_data.json', 1,
                                         game_time_window, scores_demo)
    assert expected_log == scores_sim.get_id_log()

    examine_demo = ["pick up toonie", "examine toonie"]
    expected_log = [1, 1, 1]
    examine_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, examine_demo)
    assert expected_log == examine_sim.get_id_log()

    interact_demo = ["go to lobby", "go outside", "go south", "go south", "go inside Bahen", "go to CSSU lounge",
                     "interact Prof Sadia", "quests", "interact Prof Sadia", "go to lobby", "go to east exit",
                     "go inside McLennan", "pick up Pocoyo", "go to south exit", "go inside bahen", "go to CSSU lounge",
                     "interact Prof Sadia", "inventory"]
    expected_log = [1, 2, 3, 4, 7, 8, 9, 9, 9, 8, 12, 13, 13, 12, 8, 9, 9]
    interact_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, interact_demo)
    assert expected_log == interact_sim.get_id_log()
