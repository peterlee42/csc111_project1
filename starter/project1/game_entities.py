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


@dataclass
class LocationEntities:
    """
    The location entities for a given location.

    Instance Attributes:
        - items: a list of items available in the location
        - visited: a boolean that indicates if the location has been visited
        - given_items: a list of items that the location can give if the player uses the correct item
    """

    items: list[str]
    given_items: list[str]
    npcs: list[str]


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - id_num: the unique identifier of the location
        - name: the name of the locations
        - descriptions: A tuple of two types of descriptions in this order. a short description for quick rederence and
                        a longer description of the location displayed upon entering
        - available_directions: a dictionary of available directions in the location
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
    location_entities: LocationEntities
    visited: bool = False


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
        - self.name != ''
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
    description: str
    start_position: int
    target_position: int
    target_points: int


@dataclass
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
        - self.quest_messages[1] != ''
        - self.required_items != []
        - self.reward != ''
    """

    name: str
    description: str
    location_id: int
    quest_messages: tuple[str, str]
    required_items: list[str]
    reward: str
    is_quest_completed: bool = False


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

    def use(self, current_location: Location, item_obj: Optional[Item]) -> bool:
        """Use an item in the player's inventory. Return true if the player sucessfully used the item. Return false
        otherwise.

        Precondition:
        - not item_obj and item_name == item_obj.name
        """
        if not item_obj or item_obj.name not in self.inventory:
            print(self._get_random_message(
                'item_does_not_exist'))
            return False
        elif current_location.id_num == item_obj.target_position:
            item_name = item_obj.name
            print(self._get_random_message('item_used', item_name))

            random_index = randrange(len(current_location.location_entities.given_items))
            given_item = current_location.location_entities.given_items[random_index]
            self.score += item_obj.target_points
            self.inventory.remove(item_name)
            self.inventory.append(given_item)
            print(f'You received: {given_item}')
            return True
        else:
            item_name = item_obj.name
            print(self._get_random_message(
                'item_cannot_be_used'), item_name)
            return False

    def drop_item(self, current_location: Location, item_name: str) -> bool:
        """Remove an item from the player's inventory. Return true if the player sucessfully dropped the item.
        Return false otherwise.
        """
        for inventory_item in self.inventory:
            if item_name == inventory_item.lower():
                self.inventory.remove(inventory_item)
                current_location.location_entities.items.append(inventory_item)

                self.score -= 1  # so that you cant infinitely farm points

                print(self._get_random_message(
                    'item_removed_from_inventory', inventory_item))

                return True

        print(self._get_random_message('item_does_not_exist', item_name))
        return False

    def go(self, current_location: Location, direction: str) -> int:
        """Return the id of the new location if the direction is valid. Return otherwise, return False.
        """
        for loc_direction in current_location.available_directions:
            if direction == loc_direction.lower():
                return current_location.available_directions[direction]

        print("Looks like that isn't a valid direction...")
        return current_location.id_num

    def pick_up_item(self, current_location: Location, item_name: str) -> bool:
        """Add an item to the player's inventory. Reward the player with 1 point. Return true if the player sucessfully
        picked up the item. Return false otherwise.
        """
        for loc_item in current_location.location_entities.items:
            if item_name == loc_item.lower():

                self.inventory.append(loc_item)  # add to inventory
                # remove item from location
                current_location.location_entities.items.remove(loc_item)

                # add 1 point to score for picking up item
                self.score += 1

                print(self._get_random_message('item_picked_up', loc_item))
                return True

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

    def examine_item(self, item_obj: Optional[Item]) -> bool:
        """Examine the item and display the item's description. Return true if the player sucessfully examined the item.
        Return false otherwise.

        Precondition:
        - not item_obj and item_name == item_obj.name
        """

        if item_obj.name in self.inventory:
            print(item_obj.description)
            return True
        else:
            print(self._get_random_message(
                'item_does_not_exist'))
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

    def interact(self, current_location_id: int, npc: Npc) -> bool:
        """Handle interaction with the NPC. Return True if interaction is successful, False otherwise."""
        if current_location_id == npc.location_id:
            if npc.is_quest_completed:
                print(f"{npc.name} says: '{npc.quest_messages[1]}'")
                return True
            elif npc.quest_messages[0] in self.quests:
                is_quest_complete = self.complete_quest(npc)
                if is_quest_complete:
                    print(
                        f"{npc.name} says: '{npc.quest_messages[1]}'\nYou received: {npc.reward}")
                    return True
                else:
                    print(
                        f"You have already spoken to {npc.name}.\nFinish the quest and interact again when completed.")
                    return False
            else:
                print(f"{npc.name} says: '{npc.quest_messages[0]}'")
                print("Finish the quest and interact again when completed.")
                self.quests.append(npc.quest_messages[0])
                return True
        print("Doesn't seem like that person is here...")
        return False

    def complete_quest(self, npc: Npc) -> bool:
        """Check if the player has all the required items to complete the quest."""
        if all(item in self.inventory for item in npc.required_items):
            npc.is_quest_completed = True
            self.inventory.append(npc.reward)  # Give the reward
            self.score += 15  # Add score (assuming a fixed value)

            for required_item in npc.required_items:
                self.inventory.remove(required_item)

            self.quests.remove(npc.quest_messages[0])  # Remove the quest
            return True
        return False

    def undo_interaction(self, npc: Npc) -> None:
        """Undo the last interaction with the NPC."""
        if npc.is_quest_completed:
            self.inventory.remove(npc.reward)
            self.score -= 15  # Remove points

            for required_item in npc.required_items:
                self.inventory.append(required_item)

            self.quests.append(npc.quest_messages[0])  # Re-add the quest
            npc.is_quest_completed = False
        else:
            self.quests.remove(npc.quest_messages[0])


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
