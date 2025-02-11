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
        - descriptions: A tuple of two types of descriptions in this order. a short description for quick rederence and
                        a longer description of the location displayed upon entering
        - available_directions: a dictionary of available directions in the location
        - items: a list of items available in the location
        - visited: a boolean that indicates if the location has been visited
        - given_items: a list of items that the location can give if the player uses the correct item
        - npcs: a list of npcs (non-playable characters) in the location

    Representation Invariants:
        - self.id_num >= 0
        - self.name != ''
        - self.descriptions[0] != ''
        - self.descriptions[1] != ''
        - len(self.desciptions[0]) <= len(self.descriptions[1])
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.
    id_num: int
    name: str
    descriptions: tuple[str, str]
    available_directions: dict[str, int]
    items: list[str]
    given_items: list[str]
    npcs: list[str]
    visited: bool = False


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

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
        - self.name != ''
        - self.full_name != ''
        - self.description != ''
        - self.start_position >= 0
        - self.target_position >= 0
        - self.target_points >= 0
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


class Player:
    """A player in our text adventure game world.

    Instance Attributes:
        - inventory: a list of items the player has
        - available_commands: a list of actions that the player can use
        - score: type player's score so far
        - quests: a list of all quests that the player accepted

    Representation Invariants:
        - self.score >= 0
    """

    # Private Instance Attributes:
    # - _messages: a dictionary mapping all types of output messages to a list of output messages of that type.

    _messages: dict[str, list[str]]
    inventory: list[str]
    available_actions: list[str]
    score: int
    quests: list[str]

    def __init__(self, message_data_file: str) -> None:
        """Initialize a new player object."""
        self.inventory = []
        self.available_actions = ['go', 'pick up',
                                  'use', 'drop', 'examine', 'interact']
        self.score = 0
        self.quests = []

        # Message data
        self._messages = self._load_message_data(message_data_file)

    @staticmethod
    def _load_message_data(filename: str) -> dict[str, list[str]]:
        """Load messages from a JSON file with the given filename and
        return dictionary mapping all types of message to a list of the messages of that type."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        game_messages = {}
        # Go through each element associated with the 'message_types' key in the file
        # Map each type of message to the list of all messages of that type.
        for message_type in data['message_types']:
            game_messages[message_type['type']] = message_type['messages']

        return game_messages

    def _get_random_message(self, message_type: str, target: Optional[str] = None) -> str:
        """Get a random message from the messages attribute based on the message type.
        If the message does not exist, raise an error

        Preconditions:
        - target is not None and any({'{target}' in message for message in self._messages[message_type]})
        """
        if message_type in self._messages:
            random_index = randrange(len(self._messages[message_type]))
            random_message = self._messages[message_type][random_index]

            if not target:
                return random_message
            else:
                formatted_message = random_message.format(target=target.title())
                return formatted_message[0].upper() + formatted_message[1:]
        raise ValueError('This message type does not exist.')

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
        """Return the id of the new location if the direction is valid. Return otherwise, return False.
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
        """Display all the player's current quests"""
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
        - location_id: the location where the NPC is found
        - quest_messages: a tuple containing the quest message and the quest completion message
        - required_items: A list of items required to complete the quest.
        - reward: the reward given when the quest is completed
        - is_quest_completed: whether the quest has been completed

    Representation Invariants:
        - self.name != ''
        - self.description != ''
        - self.quest_messages[0] != ''
        - self.messages[1] != ''
        - self.required_items != []
        - self.reward != ''
    """

    name: str
    description: str
    location_id: int
    quest_messages: tuple[str, str]
    required_items: list[str]
    reward: str
    is_quest_completed: bool

    def __init__(self, name: str, description: str, location_id: int,
                 quest_messages: tuple[str, str],
                 required_items: list[str], reward: str) -> None:
        """Initialize the NPC."""
        self.name = name
        self.description = description
        self.location_id = location_id
        self.quest_messages = quest_messages
        self.required_items = required_items
        self.reward = reward
        self.is_quest_completed = False

    def interact(self, current_location_id: int, player: Player) -> bool:
        """Handle interaction with the NPC. Return True if interaction is successful, False otherwise."""
        if current_location_id == self.location_id:
            if self.is_quest_completed:
                print(f"{self.name} says: '{self.quest_messages[1]}'")
                return True
            elif self.quest_messages[0] in player.quests:
                is_quest_complete = self.complete_quest(player)
                if is_quest_complete:
                    print(
                        f"{self.name} says: '{self.quest_messages[1]}'\nYou received: {self.reward}")
                    return True
                else:
                    print(
                        f"You have already spoken to {self.name}. Finish the quest and interact again.")
                    return False
            else:
                print(f"{self.name} says: '{self.quest_messages[0]}'")
                player.quests.append(self.quest_messages[0])
                return True
        else:
            print("Doesn't seem like that person is here...")
            return False

    def complete_quest(self, player: Player) -> bool:
        """Check if the player has all the required items to complete the quest."""
        if all(item in player.inventory for item in self.required_items):
            self.is_quest_completed = True
            player.inventory.append(self.reward)  # Give the reward
            player.score += 15  # Add score (assuming a fixed value)

            for required_item in self.required_items:
                player.inventory.remove(required_item)

            player.quests.remove(self.quest_messages[0])  # Remove the quest
            return True
        return False

    def undo_interaction(self, player: Player) -> None:
        """Undo the last interaction with the NPC."""
        if self.is_quest_completed:
            player.inventory.remove(self.reward)
            player.score -= 15  # Remove points

            for required_item in self.required_items:
                player.inventory.append(required_item)

            player.quests.append(self.quest_messages[0])  # Re-add the quest
            self.is_quest_completed = False
        else:
            if self.quest_messages[0] in player.quests:
                player.quests.remove(self.quest_messages[0])


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
