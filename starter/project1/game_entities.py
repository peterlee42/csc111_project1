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
from typing import Optional


@dataclass
class LocationEntities:
    """
    The location entities for a given location.

    Instance Attributes:
        - items: a list of items in the given location
        - given_items: a list of items that the given location can give if the player uses the correct item
        - npcs: a list of npcs (non-playable characters) in the given location
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
        - descriptions: A tuple of two types of descriptions in this order. a short description for quick reference and
                        a longer description of the location displayed upon entering
        - available_directions: a dictionary of available directions in the location
        - location_entities: all entities in the location

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
        - name: the name of the item
        - description: a description of the item
        - start_position: the ID of the starting location of this item
        - target_position: the ID of the location that this item can be used
        - target_points: points awarded when the item is used at the location with the ID of the target position

    Representation Invariants:
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
        - dialgoue: the dialogue with the NPC
        - location_id: the location where the NPC is found
        - quest_messages: a tuple containing the quest message and the quest completion message
        - required_items: a list of items required to complete the quest.
        - reward: a list of rewarded items when the quest is completed
        - is_quest_completed: a boolean representing whether the quest has been completed

    Representation Invariants:
        - self.name != ''
        - self.dialogue != ''
        - self.quest_messages != ('', '')
        - self.required_items != []
        - self.reward != []
    """

    name: str
    dialogue: str
    location_id: int
    quest_messages: tuple[str, str]
    required_items: list[str]
    reward: list[str]
    is_quest_completed: bool = False


class Player:
    """A player in our text adventure game world.

    Instance Attributes:
        - inventory: a list of items the player is carrying
        - available_commands: a list of actions that the player can perform
        - score: the player's score so far
        - quests: a list of all quests that the player has accepted

    Representation Invariants:
        - self.score >= 0
    """

    inventory: list[str]
    available_actions: list[str]
    score: int
    quests: list[str]

    def __init__(self) -> None:
        """Initialize a new player object."""
        self.inventory = []
        self.available_actions = ['go', 'pick up', 'use', 'drop', 'examine', 'interact']
        self.score = 0
        self.quests = []

    def use(self, current_location: Location, item_obj: Optional[Item]) -> bool:
        """Use an item in the player's inventory. Return True if the player sucessfully used the item. Return False
        otherwise."""
        if not item_obj or item_obj.name not in self.inventory:
            print("You reach out, but grasp only empty air.")
            return False
        elif current_location.id_num == item_obj.target_position:
            item_name = item_obj.name
            print(f"You have used {item_name}.")

            for item in current_location.location_entities.given_items:
                self.inventory.append(item)
                print(f'You received: {item}')

            self.score += item_obj.target_points
            self.inventory.remove(item_name)

            return True
        else:
            item_name = item_obj.name
            print(f"Hmmm... Maybe {item_name} has a better use.")
            return False

    def drop_item(self, current_location: Location, item_name: str) -> bool:
        """Remove an item from the player's inventory. Return True if the player sucessfully dropped the item.
        Return False otherwise.
        Preconditions:
        - item_name == item_name.lower()
        """
        for inventory_item in self.inventory:
            if item_name == inventory_item.lower():
                self.inventory.remove(inventory_item)
                current_location.location_entities.items.append(inventory_item)

                self.score -= 1  # so that you cant infinitely farm points

                print(f"{inventory_item} has been removed from your inventory.")

                return True

        print("You reach out, but grasp only empty air.")
        return False

    def go(self, current_location: Location, direction: str) -> int:
        """Return the id of the new location if the direction is valid. Otherwise, return the current location id.
        """
        for loc_direction in current_location.available_directions:
            if direction == loc_direction.lower():
                return current_location.available_directions[loc_direction]

        print("Looks like that isn't a valid direction...")
        return current_location.id_num

    def pick_up_item(self, current_location: Location, item_name: str) -> bool:
        """Add an item to the player's inventory. Reward the player with 1 point. Return True if the player sucessfully
        picked up the item. Return False otherwise.

        Preconditions:
        - item_name == item_name.lower()
        """
        for loc_item in current_location.location_entities.items:
            if item_name == loc_item.lower():

                self.inventory.append(loc_item)  # add to inventory
                # remove item from location
                current_location.location_entities.items.remove(loc_item)

                # add 1 point to score for picking up item
                self.score += 1

                print(f"{loc_item} has been added to your inventory.")
                return True

        print("You reach out, but grasp only empty air.")
        return False

    def display_inventory(self) -> None:
        """Displays the player's current inventory in sorted order"""
        if not self.inventory:
            print("Your inventory is empty!")
        else:
            sorted_inventory = sorted(self.inventory)
            print("You currently have:")
            for item in sorted_inventory:
                print('- ', item)

    def examine_item(self, item_obj: Optional[Item]) -> bool:
        """Examine the item and display the item's description. Return True if the player sucessfully examined the item.
        Return False otherwise.
        """
        if not item_obj or item_obj.name not in self.inventory:
            print("You reach out, but grasp only empty air.")
            return False
        else:
            print(item_obj.description)
            return True

    def display_quests(self) -> None:
        """Display all the player's current quests in sorted order"""
        if not self.quests:
            print("You have no quests.")
        else:
            sorted_quests = sorted(self.quests)
            print("You currently undertook these quests:")
            for item in sorted_quests:
                print('- ', item)

    def interact(self, current_location_id: int, npc: Npc, rewarded_points: int) -> bool:
        """Handle interaction with the NPC. Return True if interaction is successful, False otherwise."""
        if current_location_id != npc.location_id:
            print("Doesn't seem like that person is here...")
            return False

        if npc.is_quest_completed:
            print(f"{npc.name} says: 'Thanks again for the help!'")
            return True

        if self.complete_quest(npc, rewarded_points):
            if npc.quest_messages[0] not in self.quests:
                print(f"{npc.name} says: '{npc.dialogue}'\n")

            print(f"{npc.name} says: '{npc.quest_messages[1]}'")
            print("You received:")
            for item in npc.reward:
                print('-', item)
            self.quests.append(npc.quest_messages[0])
            return True
        else:
            if npc.quest_messages[0] not in self.quests:
                self.quests.append(npc.quest_messages[0])
            print(f"{npc.name} says: '{npc.dialogue}'")
            print('\nFinish the quest and interact again when completed.')
            return True

    def complete_quest(self, npc: Npc, rewarded_points: int) -> bool:
        """Check if the player has all the required items to complete the quest."""
        for item in npc.required_items:
            if item not in self.inventory:
                return False

        npc.is_quest_completed = True
        for reward in npc.reward:
            self.inventory.append(reward)  # Give the reward
        self.score += rewarded_points
        for required_item in npc.required_items:
            self.inventory.remove(required_item)

        if npc.quest_messages[0] in self.quests:
            self.quests.remove(npc.quest_messages[0])  # Remove the quest
        return True

    def undo_interaction(self, npc: Npc) -> None:
        """Undo the last interaction with the NPC."""
        if npc.is_quest_completed:
            for reward in npc.reward:
                self.inventory.remove(reward)
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
