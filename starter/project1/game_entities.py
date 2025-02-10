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
# import difflib


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: the unique identifier of the location
        - name: the name of the locations
        - brief_description: a short description for quick rederence
        - long_description: a longer description of the location displayed upon entering
        - available_directions: a dictionary of available directions in the location
        - items: a list of items available in the location
        - visited: a boolean that indicates if the location has been visited
        - given_items: a list of items that the location can give if the player uses the correct item

    Representation Invariants:
        - self.id_num >= 0
        - self.name != ''
        - self.brief_description != ''
        - self.long_description != ''
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
    given_items: list[str]
    visited: bool = False

    # def __init__(self, location_id, name, brief_description, long_description, available_directions, items,
    #              given_items, visited=False) -> None:
    #     """Initialize a new location.
    #
    #     # Add more details here about the initialization if needed
    #     """
    #
    #     self.id_num = location_id
    #     self.name = name
    #     self.brief_description = brief_description
    #     self.long_description = long_description
    #     self.available_directions = available_directions
    #     self.items = items
    #     self.visited = visited
    #     self.given_items = given_items


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here
        - name: the name of the item
        - full_name: the full name of the item
        - description: a description of the item
        - start_position:
        - target_position:
        - target_points: points awarded when the item is placed at its correct location
        - item_type: the type of item (ie a consumable, tool, etc)

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
        - self.name != ''
        - self.full_name != ''
        - self.description != ''
        - self.start_position >= 0
        - self.target_position >= 0
        - self.target_points >= 0
        - self.item_type != ''
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    full_name: str
    description: str
    start_position: int
    target_position: int
    target_points: int
    item_type: str


class Player:
    """A player in our text adventure game world.

    Instance Attributes:
        - inventory: a list of items the player has
        - available_commands: a list of actions that the player can use
        - score: type player's score so far
        - messages: the output messages that the player receives after doing an action
        - quests: a list of all quests that the player accepted

    Representation Invariants:
        - self.current_location_id >= 0
        - self.score >= 0
    """
    inventory: list[str]
    available_actions: list[str]
    score: int
    messages: dict[str, list[str]]
    quests: list[str]

    def __init__(self) -> None:
        """Initialize a new player object."""
        self.inventory = []
        self.available_actions = ['go', 'pick up',
                                  'use', 'drop', 'examine', 'interact']
        self.score = 0
        self.messages = self._load_player_messages('player_messages.json')
        self.quests = []

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

    def use(self, current_location: Location, item_name: str, item_obj: Optional[Item]) -> bool:
        """Use an item in the player's inventory. Return true if the player sucessfully used the item. Return false
        otherwise.

        Precondition:
        - not item_obj and item_name == item_obj.name
        """
        # if item_name not in self.inventory:
        #     # Attempt fuzzy matching in the player's inventory.
        #     corrected = difflib.get_close_matches(
        #         item_name, self.inventory, n=1, cutoff=7)
        #     if corrected:
        #         corrected_item = corrected[0]
        #         print(f"Interpreting '{item_name}' as '{corrected_item}'.")
        #         item_name = corrected_item

        if item_name not in self.inventory:
            print(self._get_random_message(
                'item_does_not_exist', item_name))
            return False
        elif current_location.id_num == item_obj.target_position:
            print(self._get_random_message('item_used', item_name))

            random_index = randrange(len(current_location.given_items))
            given_item = current_location.given_items[random_index]
            self.score += item_obj.target_points
            self.inventory.remove(item_name)
            self.inventory.append(given_item)
            print(f'You received: {given_item}')
            return True
        else:
            print(self._get_random_message(
                'item_cannot_be_used', item_name))
            return False

    def drop_item(self, current_location: Location, item_name: str) -> bool:
        """Remove an item from the player's inventory. Return true if the player sucessfully dropped the item.
        Return false otherwise.
        """
        # if item_name not in self.inventory:
        #     corrected = difflib.get_close_matches(
        #         item_name, self.inventory, n=1, cutoff=0.7)
        #     if corrected:
        #         corrected_item = corrected[0]
        #         print(f"Interpreting '{item_name}' as '{corrected_item}'.")
        #         item_name = corrected_item
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            current_location.items.append(item_name)

            self.score -= 1  # so that you cant infinitely farm points

            print(self._get_random_message(
                'item_removed_from_inventory', item_name))
            return True
        else:
            print(self._get_random_message('item_does_not_exist', item_name))
            return False

    def go(self, current_location: Location, direction: str) -> int:
        """Return the id of the new location if the direction is valid. Return the current location id otherwise.
        """
        if direction in current_location.available_directions:
            return current_location.available_directions[direction]
        else:
            # possible_dirs = list(current_location.available_directions.keys())
            # corrected = difflib.get_close_matches(
            #     direction, possible_dirs, n=1, cutoff=0.7)
            # if corrected:
            #     corrected_direction = corrected[0]
            #     print(
            #         f"Interpreting '{direction}' as '{corrected_direction}'.")
            #     return current_location.available_directions[corrected_direction]
            # else:
            print("Looks like that isn't a valid direction...")
            return current_location.id_num

    def pick_up_item(self, current_location: Location, item_name: str) -> bool:
        """Add an item to the player's inventory. Reward the player with 1 point. Return true if the player sucessfully
        picked up the item. Return false otherwise.
        """

        # if item_name not in current_location.items:
        #     corrected = difflib.get_close_matches(
        #         item_name, current_location.items, n=1, cutoff=0.7)
        #     if corrected:
        #         corrected_item = corrected[0]
        #         print(f"Interpreting '{item_name}' as '{corrected_item}'.")
        #         item_name = corrected_item
        if item_name in current_location.items:

            self.inventory.append(item_name)  # add to inventory
            # remove item from location
            current_location.items.remove(item_name)

            # add 1 point to score for picking up item
            self.score += 1

            print(self._get_random_message('item_picked_up', item_name))
            return True
        else:
            print(self._get_random_message('item_does_not_exist', item_name))
            return False

    def display_inventory(self) -> None:
        """Displays the player's current inventory in sorted order"""
        if not self.inventory:
            print(self._get_random_message('inventory_empty'))
        else:
            sorted_inventory = sorted(self.inventory)
            print(self._get_random_message('currently_have'))
            for item in sorted_inventory:
                print('- ', item)

    def examine_item(self, item_name: str, item_obj: Optional[Item]) -> bool:
        """Examine the item and display the item's description. Return true if the player sucessfully examined the item.
        Return false otherwise.

        Precondition:
        - not item_obj and item_name == item_obj.name
        """
        # if item_name not in self.inventory:
        #     corrected = difflib.get_close_matches(
        #         item_name, self.inventory, n=1, cutoff=0.7)
        #     if corrected:
        #         corrected_item = corrected[0]
        #         print(f"Interpreting '{item_name}' as '{corrected_item}'.")
        #         item_name = corrected_item
        if item_name in self.inventory:
            print(item_obj.description)
            return True
        else:
            print(self._get_random_message(
                'item_does_not_exist', item_name))
            return False

    def display_quests(self) -> None:
        """Display all of the player's current quests"""
        if not self.quests:
            print("You have no quests.")
        else:
            sorted_quests = sorted(self.quests)
            print("You currently undertook these quests:")
            for item in sorted_quests:
                print('- ', item)


class Npc:
    """An NPC (Non-Player Character) that assigns and completes quests in our text adventure world.
    Instance Attributes:
        - name: the name of the NPC
        - description: the description of the NPC
        - quest: the quest the NPC gives to the player
        - required_items: list of items required to complete the quest
        - reward: the reward given when the quest is completed
        - is_quest_completed: whether the quest has been completed
        - points: the number of points given when the quest has been completed
        - taken_item_index: keeps track of the index of the taken items in the player's inventory

    Representation Invariants:
        - self.name != ''
        - self.description != ''
        - self.quest != ''
        - self.required_items != []
        - self.reward != ''
        - self.points > 0
        - all({index >= 0 for index in taken_item_index})
    """

    name: str
    description: str
    location_id: int
    quest: str
    quest_complete_message: str
    required_items: list[str]
    reward: str
    is_quest_completed: bool
    points: int
    taken_item_index: list[int]

    def __init__(self, name: str, description: str, location_id: int,
                 quest: str, quest_complete_message: str, required_items: list[str], reward: str) -> None:
        """Initialize the NPC"""
        self.name = name
        self.description = description
        self.location_id = location_id
        self.quest = quest
        self.quest_complete_message = quest_complete_message
        self.required_items = required_items
        self.reward = reward
        self.is_quest_completed = False
        self.interacted = False
        self.points = 15
        self.taken_item_index = []

    def interact(self, current_location_id: int, player: Player) -> bool:
        """Handle interaction with the NPC. Return true if the interaction is successful. False otherwise."""
        if current_location_id == self.location_id:
            if self.is_quest_completed:
                print(f"{self.name} says: '{self.quest_complete_message}'")
                return True
            elif self.interacted:
                is_quest_complete = self.complete_quest(player)
                if is_quest_complete:
                    print(
                        f"{self.name} says: '{self.quest_complete_message}'\nYou received: {self.reward}")
                    return True
                else:
                    print(f"You have already spoken to {self.name}. Finish the quest and interact again.")
                    return False
            else:
                print(f"{self.name} says: '{self.quest}'")
                self.interacted = True
                player.quests.append(self.quest)
                return True
        else:
            print("Doesn't seem like that person is here...")
            return False

    def complete_quest(self, player: Player) -> bool:
        """Check if the player has all the required items to complete the quest."""
        items_found = all({item in player.inventory for item in self.required_items})
        if items_found:
            # The player has completed the quest!
            self.is_quest_completed = True
            # Give the reward
            player.inventory.append(self.reward)
            player.score += self.points  # Add score

            for required_item in self.required_items:
                self.taken_item_index.append(
                    player.inventory.index(required_item))
                player.inventory.remove(required_item)

            player.quests.remove(self.quest)  # remove the quest

            return True
        return False

# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.


if __name__ == "__main__":
    # pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
