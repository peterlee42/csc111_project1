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

        menu = ["look", "inventory", "score", "undo", "log", "quit", "quests"]
        initial_location_id = current_location.id_num
        game_win_items = ['laptop', 'laptop charger', 'lucky UofT mug', 'USB drive']

        for command in commands:
            if command in menu:
                if command == "log":
                    self._events.display_events()
                elif command == "quit":
                    print('Bye bye!')
                    self._game.ongoing = False
                elif command == "undo":
                    self._game.undo(self._events)
                elif command == "inventory":
                    self._game.player.display_inventory()
                elif command == "score":
                    print("Score:", self._game.player.score)
                elif command == "look":
                    print(current_location.descriptions[1])
                elif command == "quests":
                    self._game.player.display_quests()
            else:
                self.run_event_command(command, initial_location_id, game_win_items, current_location)
                current_location = self._game.get_location()

    def run_event_command(self, command: str, initial_location_id: int, game_win_items: list[str],
                          current_location: Location) -> None:
        """This will only run a command if it is not a menu command. This method will run the non-menu command and
        update self._events accordingly.
        Preconditions:
        - command not in ["look", "inventory", "score", "undo", "log", "quit", "quests"]
        """
        command = command.lower().strip()
        player_action, player_target = parse_command(command, self._game.player.available_actions)
        action_time = 0
        if player_action == 'go':
            result = self._game.player.go(current_location, player_target)

            # add to time if it is a new location
            if self._game.current_location_id != result:
                action_time = 6
            self._game.current_location_id = result
            current_location = self._game.get_location()
        elif player_action == 'pick up':
            self._game.player.pick_up_item(current_location, player_target)
            action_time = 2
        elif player_action == 'use':
            player_target_obj = self._game.get_item(player_target)
            self._game.player.use(current_location, player_target_obj)
            action_time = 3
        elif player_action == 'drop':
            self._game.player.drop_item(current_location, player_target)
            action_time = 2
        elif player_action == 'examine':
            player_target_obj = self._game.get_item(player_target)
            self._game.player.examine_item(player_target_obj)
            action_time = 2
        elif player_action == 'interact':
            target_npc_obj = self._game.get_npc(player_target)
            rewarded_points = sum(
                [self._game.get_item(item).target_points for item in target_npc_obj.required_items
                 if target_npc_obj])
            self._game.player.interact(self._game.current_location_id, target_npc_obj, rewarded_points)
            action_time = 5

        # If it's a valid move, then add minutes and check if time has passed the deadline.
        player_lost = self._game.add_minutes(action_time)
        # Checks if the player has won
        self._game.check_win(initial_location_id, player_lost, game_win_items)

        self._events.add_event(
            Event(current_location.id_num, current_location.descriptions[0],
                  self._game.time_window.current_time),
            command)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.

        >>> sim_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
        >>> sim = AdventureGameSimulation('game_data.json', 1, sim_time_window, ["go to lobby", "go outside", "go south", 'go inside McLennan', 'pick up pocoyo'])
        Pocoyo has been added to your inventory.
        >>> sim.get_id_log()
        [1, 2, 3, 4, 13, 13]

        >>> sim_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
        >>> sim = AdventureGameSimulation('game_data.json', 1, sim_time_window, ["pick up tOOnie", "score", "go to lobby", "use toonie", "score", "go to dorm"])
        toonie has been added to your inventory.
        Score: 1
        You have used toonie.
        You received: Red Bull
        Score: 11
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
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })

    # Win Demo
    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
    win_walkthrough = ["pick up toonie", "pick up five dollar bill", "go to lobby", "use toonie", "go outside",
                       "go south", "go inside McLennan", "pick up Pocoyo", "go to west exit",
                       "go to food trucks", "use five dollar bill", "go back", "go south",
                       "go inside Bahen", "go to CSSU lounge",
                       "interact Prof Sadia", "go to lobby", "go to east exit",
                       "go east", "go north", "go north", "go north", "go north", "go inside Myhal Centre",
                       "pick up student ID", "pick up backpack", "go outside myhal centre", "go south",
                       "go inside New College",
                       "interact Alex Carter", "go east exit", "go south", "go south", "go south", "go east",
                       "go south", "go west", "go inside Gerstein", "interact Security Guard", "go outside", "go east",
                       "go north", "go west", "go north", "go north", "go north", "go north", "go east",
                       "go inside Robarts", "pick up barista notes", "go to Robarts Commons", "interact tired student",
                       "go to robarts cafe",
                       "interact Barista", "go downstairs", "go to lobby", "go outside", "go west", "go south",
                       "go south", "go inside Sidney Smith", "use admin pass", "go outside", "go north", "go north",
                       "go west", "go west", "go inside Chestnut", "go to dorm"]
    expected_log = [1, 1, 1, 2, 2, 3, 4, 13, 13, 4, 6, 6, 4, 7, 8, 9, 9, 8, 12, 14, 16, 23, 25, 29, 30, 30, 30, 29, 25,
                    27, 27, 25, 23, 16, 14, 15, 17, 18, 20, 20, 18, 17, 15, 14, 16, 23, 25, 29, 31, 32, 32, 33, 33, 34,
                    34, 33, 32, 31, 29, 25, 23, 24, 24, 23, 25, 29, 28, 3, 2, 1]
    win_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, win_walkthrough)
    assert expected_log == win_sim.get_id_log()

    # Lose Demo
    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
    lose_demo = ["go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm", "go to lobby", "go to dorm", "go to lobby", "go to dorm",
                 "go to lobby", "go to dorm"]
    expected_log = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
                    1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
                    1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    lose_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, lose_demo)
    assert expected_log == lose_sim.get_id_log()

    # Inventory demo
    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
    inventory_demo = ["pick up toonie", "inventory", "go to lobby", "use toonie", "inventory"]
    expected_log = [1, 1, 2, 2]
    inventory_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, inventory_demo)
    assert expected_log == inventory_sim.get_id_log()

    # Scores demo
    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
    scores_demo = ["pick up toonie", "score", "go to lobby", "use toonie", "score"]
    expected_log = [1, 1, 2, 2]
    scores_sim = AdventureGameSimulation('game_data.json', 1,
                                         game_time_window, scores_demo)
    assert expected_log == scores_sim.get_id_log()

    # Examine demo
    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
    examine_demo = ["pick up toonie", "examine toonie"]
    expected_log = [1, 1, 1]
    examine_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, examine_demo)
    assert expected_log == examine_sim.get_id_log()

    # Interact demo
    game_time_window = TimeWindow(time(hour=8, minute=0), time(hour=16, minute=0))
    interact_demo = ["go to lobby", "go outside", "go south", "go south", "go inside Bahen", "go to CSSU lounge",
                     "interact Prof Sadia", "quests", "interact Prof Sadia", "go to lobby", "go to east exit",
                     "go inside McLennan", "pick up Pocoyo", "go to south exit", "go inside bahen", "go to CSSU lounge",
                     "interact Prof Sadia", "inventory"]
    expected_log = [1, 2, 3, 4, 7, 8, 9, 9, 9, 8, 12, 13, 13, 12, 8, 9, 9]
    interact_sim = AdventureGameSimulation('game_data.json', 1, game_time_window, interact_demo)
    assert expected_log == interact_sim.get_id_log()
