# CSC111 Winter 2025 Project 1

### Peter Lee and Akshar Patel

### March 16, 2025

## Running the game

We should be able to run your game by simply running `adventure.py`. If
you have any other requirements (e.g., installing certain modules),
describe them here. Otherwise, skip this section.

Requirements: You need the datetime library.

## Game Map

Example game map below:

     -1  1  -1  -1  -1  34
     -1  2  -1  30  -1  33
     -1  3  28  29  31  32
     -1  |  27  25  -1  -1
     -1  |  -1  23  24  -1
      6  4  13  16  -1  -1
     -1  7  |   |   -1  -1
     -1  8  12  14  15  22
     -1  9  -1  -1  |   -1
     -1 -1  20  18  17  -1
     -1 -1  -1  -1  19  -1
     -1 -1  -1  -1  21  -1

Where there is a: $|$

-   $|$ means that the locations above and below it are connected, so
    that the player can move between them without needing to go to a
    location in between.

-   For example, the player can move between location 3 and location 4.

Starting location is: 1
## Game solution


List of commands:
```
[”pick up toonie”, ”pick up five dollar bill”, ”go to lobby”, ”use toonie”, ”go outside”, ”go south”,
”go inside McLennan”, ”pick up Pocoyo”, ”go to east exit”, ”go to food trucks”, ”use five dollar
bill”, ”go back”, ”go south”, ”go inside Bahen”, ”go to CSSU lounge”, ”interact Prof Sadia”, ”go
to lobby”, ”go to east exit”, ”go east”, ”go north”, ”go north”, ”go north”, ”go north”, ”go inside
Myhal Centre”, ”pick up student ID”, ”pick up backpack”, ”go outside myhal centre”, ”go south”,
”go inside New College”, ”interact Alex Carter”, ”go west exit”, ”go south”, ”go south”, ”go south”,
”go east”, ”go south”, ”go west”, ”go inside Gerstein”, ”interact Security Guard”, ”go outside”,
”go east”, ”go north”, ”go west”, ”go north”, ”go north”, ”go north”, ”go north”, ”go east”, ”go
inside Robarts”, ”pick up barista notes”, ”go to Robarts Commons”, ”interact tired student”, ”go
to robarts cafe”, ”interact Barista”, ”go downstairs”, ”go to lobby”, ”go outside”, ”go west”, ”go
south”, ”go south”, ”go inside Sidney Smith”, ”use admin pass”, ”go outside”, ”go north”, ”go
north”, ”go west”, ”go west”, ”go inside Chestnut”, ”go to dorm”]
```

## Lose condition(s)

`time_window` attribute in the `AdventureGame` class. The `time_window`
is of type `TimeWindow` which has the attributes `current_time` and
`deadline`. As the player performs an action, `current_time` will keep
passing. If `current_time` passes `deadline` (which is an attribute
found in the TimeWindow dataclass), the player loses the game. We check
wins and losses in the `check_win` method in the `AventureGame` class.

List of commands:
```
[”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to
lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go
to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”,
”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to
lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go
to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”,
”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to
lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go
to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”,
”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to
lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go
to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”, ”go to lobby”, ”go to dorm”]
```
Which parts of your code are involved in this functionality:

-   `AdventureGame` class in `adventure.py`

-   `time_window` attribute in `AdventureGame` class

-   `TimeWindow` dataclass in `adventure.py`

-   `check_win` method in the `AdventureGame` class

## Inventory

1.  All location IDs that involve items in the game: Below are all the
    location id's that are associated with an item.

2.  Item data:

    1.  For Item 1:

        -   Item name: USB drive

        -   Item start location ID: 24

        -   Item target location ID: 1

    2.  For Item 2:

        -   Item name: backpack

        -   Item start location ID: 30

        -   Item target location ID: 1

    3.  For Item 3:

        -   Item name: toonie

        -   Item start location ID: 1

        -   Item target location ID: 2

    4.  For Item 4:

        -   Item name: student ID

        -   Item start location ID: 30

        -   Item target location ID: 27

    5.  For Item 5:

        -   Item name: notebook

        -   Item start location ID: 9

        -   Item target location ID: 30

    6.  For Item 6:

        -   Item name: lucky UofT mug

        -   Item start location ID: 35

        -   Item target location ID: 1

    7.  For Item 7:

        -   Item name: laptop charger

        -   Item start location ID: 20

        -   Item target location ID: 1

    8.  For Item 8:

        -   Item name: laptop

        -   Item start location ID: 27

        -   Item target location ID: 1

    9.  For Item 9:

        -   Item name: Red Bull

        -   Item start location ID: 2

        -   Item target location ID: 33

    10. For Item 10:

        -   Item name: crumpled paper

        -   Item start location ID: 20

        -   Item target location ID: 32

    11. For Item 11:

        -   Item name: admin pass

        -   Item start location ID: 33

        -   Item target location ID: 24

    12. For Item 12:

        -   Item name: chicken burger

        -   Item start location ID: 6

        -   Item target location ID: 20

    13. For Item 13:

        -   Item name: Pocoyo

        -   Item start location ID: 13

        -   Item target location ID: 9

    14. For Item 14:

        -   Item name: five dollar bill

        -   Item start location ID: 1

        -   Item target location ID: 6

3.  Exact command(s) that should be used to pick up an item (choose any
    one item for this example), and the command(s) used to use/drop the
    item

    Chosen item: $toonie$

    -   $>>>$ pick up $toonie$

    -   $>>>$ drop $toonie$

    -   $>>>$ use $toonie$

4.  Which parts of your code (file, class, function/method) are involved
    in handling the `inventory` command:

    When handling the inventory command, the files involved are in
    `game_entities.py`. Within this file, there is a class called
    `Player`. The command handling inventory is under the
    `display_inventory` method in the `Player` class.

    We run this method in the `if __name__ == __main__` block in
    `adventure.py` file


## Score

Briefly describe the way players can earn scores in your game. Include
the first location in which they can increase their score, and the exact
list of command(s) leading up to the score increase:

Players will earn points throughout the game. They will gain one point
for picking up an item. Dropping an item will forfeit that point and the
player's score will decrease by one; this is so that the player will not
be able to infinitely gain points. Using the correct item in target
locations will also earn the player points. These points vary based on
the item. Additionally, interacting with NPCs (non-playable characters)
and fulfilling their quests will give the player 15 points per completed
quest. The first time that the player will have a chance to earn one
point right when they start the game. They will start in their dorm
which has a toonie. They must do the following commands:

-   pick up $toonie$

Here the player is picking up a toonie which will immediately give the
player a point.\
Copy the list you assigned to `scores_demo` in the
`project1_simulation.py` file into this section of the report:

\[\"pick up toonie\", \"score\", \"go to lobby\", \"use toonie\",
\"score\"\]

Which parts of your code (file, class, function/method) are involved in
handling the `score` functionality:

There are two files involved in handling the score functionality:
`adventure.py` and `game_entities.py`. method `undo`. Whenever the
player uses the command Within the former, there is an `AdventureGame`
class which contains the `undo` function. If the last command the player
entered caused a gain or loss of points, `undo` will restore or remove
those points accordingly.

Within the `game_entities.py` file, there is a `Player` class, which
contains the methods used to implement the score's functionality: `use`,
`drop_item`, `pick_up_item`, `complete_quest`, and `undo_interaction`.
In each of these methods, the player's score is either increased,
decreased, or left unchanged, depending on what the player does.

## Enhancements

Time Window

-   Basic description of what the enhancement is: Instead of using
    purely score to track progress, we used the datetime library to keep
    track of the player's current time.

-   Complexity level: Medium

-   We had to create a new dataclass called TimeWindow which kept track
    of the current time and the deadline time. We also had to made our
    lose condition based in this time window. Some difficulties were
    adding minutes to the current time attribute in TimeWindow. Also, we
    had to find a way to display the 24 hours time in a more natural 12
    hour time format.

Non-playable Characters (NPC)

-   Basic description of what the enhancement is: A game entity that can
    interact with the player, give it quests, and reward items once the
    quest is completed.

-   Complexity level (low/medium/high): High

-   We had to develop a new dataclass for the NPC and make a working
    methods in the player class that would be able to interact with the
    NPC and get the correct message output (ie. if it is the player's
    first time interacting, it would prompt a different message than if
    we completed the quest). Another difficulty was trying to undo the
    interaction, which we had to make use of a new player attribute
    called quests.

Examine

-   Basic description of what the enhancement is: Lists item description
    in console

-   Complexity level (low/medium/high): low

-   It is a basic method in the player class that would print the
    descriptions of a given item in the player's inventory.

Inductive Puzzle

-   Basic description of what the enhancement is: We created a complex
    puzzle where the player has to pick up, use, examine and interact
    with various entities to win the game. Interacting with these
    entities will require the player to traverse across the map trying
    to find different items in return for information in the form of a
    riddle or items that advance them to completing the game.

-   Complexity level (low/medium/high): High

-   There are many locations that the player has to visit to find useful
    items. Also, the player must interact with non-playable characters
    to retrieve items that are used to proceed in the game. To do this,
    we implemented an Npc class, new attributes in the location
    dataclass. Namely an attribute with the type LocationEntities which
    is another dataclass we developed that has attributes including a
    list of the given location's items, given items (items it will give)
    and the non-playable characters. We also had to add many new items,
    introduce new characters, and develop new locations for this to the
    story to be plausible.

Parse Command

-   Basic description of what the enhancement is: A method which if the
    command inputed by the player is valid, it will split it into two
    parts, the 'action', and the 'target'. Otherwise, it will return a
    tuple of the original command and an empty string.

-   Complexity level (low/medium/high): Low

-   We created a simple method which takes in the command the player
    inputted, and a list of valid 'actions', such as 'go', 'interact',
    'use' etc. It will first check if the 'action' inputted by the
    player is within the list of valid actions. If it is valid the
    method will split and return the players input as two parts 'action'
    and 'target'. 'Target' is what the action is applied to, such as an
    item, location, or NPC.

## Other Things to Notes

1.  Inductive Puzzle

    -   Our puzzle is based on the gameplay. In order to complete the
        puzzle, you must follow the story and find the correct items to
        progress and unlock new items. This inductive puzzle can be
        shown in our win walkthrough simulation, where the player has to
        interact with various non-playable characters, complete quests,
        and find and use the correct items to win the game.

2.  `generate_events`

    -   We made the `simulation.py` such that it will do a real run
        through of the game. The methods we have developed under the
        class `Player` in `game_entities.py` have it so that the methods
        handle the command and print the correct output in the console
        to make our `adventure.py` file cleaner. However, this made it
        so that when we wanted to generate an event, for
        `generate_events` method under the `AdventureGameSimulation`
        class, it would inevitably print the player's action in the
        console. This means KEY player actions (which are logged in the
        `_events` attribute in `AdventureGameSimulation` ) will output
        the action in the console.
