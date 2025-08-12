#Gebeta_analysis.py
# Gebeta Game Tree Analysis

# This script analyzes the game tree of the Gebeta game, a traditional board game played in Ethiopia.
import Gebeta_game

# Initialize global variables to track game statistics
games : int = 0
awins : int = 0
bwins : int = 0
draws : int = 0
timeouts : int = 0
turns : int = 0  
agency : int = 0  


def decode_status(status: str) -> list[int]:
    """
    Decodes the game status string into a list of lists representing the game board as it is used by the Gebeta_game class.

    Args:
        status (str): The game status string to decode.

    Returns:
        list[int]: The decoded game board.
    """
    return [(ord(char) - 65) for char in status]


def encode_status(status: list[int]) -> str:
    """
    Encodes the game board into a string representation that occupies less memory.

    Args:
        status (list[int]): The game board to encode.

    Returns:
        str: The encoded game status string.
    """
    return "".join([chr(item + 65) for item in status])  # Convert the list into a string representation


def apply_to_children(file1: str, file2, player: int) -> None:
    """
    Applies game moves to all children at a given level.
    The game states from the previous level are read from the file 'file1'.
    The new game states will be written to the file 'file2'.
    Files are used because there is so much data that it does not fit into RAM.
    The player who makes the next move is needed for the Gebeta-game class.

    Args:
        file1 (str): The file containing the current game states.
        file2 (file_object): The file to write the new game states to.
        player (int): The current player (0 for Player A, 1 for Player B).
    """
    # The game statistics is stored in global variables
    global games, awins, bwins, draws, timeouts, turns, agency

    with open(file1, "r") as file_object:  # Read the data from the previous level
        for line in file_object:  # Yield a new line
            status = line.strip()  # strip whitespace
            for move in range(6):  # Make all possible moves
                if player == 1:
                    move = 5 - move  # Adjust the move for Player B
                if status[move + player * 6] == "A":  # "A" represents 0
                    continue # Try the next move if the pit is empty
                new_status = decode_status(status)  # Create a decoded copy of the current status
                new_game : Gebeta_game.Gebeta_game = Gebeta_game.Gebeta_game(new_status, player)  # Create a new game that starts at the curent status
                if new_game.move(move):  # Apply the move
                    agency += 1 if len([mov for mov in range(6) if new_game.board[mov + new_game.player * 6] > 0]) > 1 else 0  # Count the number of moves with agency (more than one valid move)
                    turns += 1  # Count the number of turns
                    print(encode_status(new_game.board), file=file2)  # Encode the new status and write it to 'file2'
                else:  # new_game.move(move) returns False if the game was completed
                    games += 1 # Increment the game count for each completed game
                    match new_game.moves[-1]:  # Get the last character to determine the game outcome
                        case "A": # Player A wins
                            awins += 1  # Count the number of games that A wins
                        case "B": # Player B wins
                            bwins += 1  # Count the number of games that B wins
                        case "D": # Draw
                            draws += 1  # Count the number of games that end in a draw
                        case "T": # Timeout due to an infinite loop
                            timeouts += 1  # Count the number of games that end in an infinite loop


def analyse_game_tree(depth: int) -> None:
    """
    Analyzes the game tree of the Gebeta game.

    Args:
        depth (int): The depth of the game tree that shall be computed
    """
    # The game statistics is stored in global variables
    global games, awins, bwins, draws, timeouts, turns, agency

    with open("results.csv", "w") as f:  # The game statistics will be written to a CSV file
        print("turns, level, games, agency, Awins, Bwins, draws, timeouts", file=f)  # Write header to CSV file
    
    # The root of the tree (level 0) is the initial game state before any move is made
    file1 = "level_0.txt"
    with open(file1, "w") as f:
        print("EEEEEEEEEEEEAA", file=f)  # Write the initial game state to the file

    # Compute all nodes of all levels up to a given depth
    for level in range(depth):  # Apply moves to the first n levels of the game tree (n = depth)
        with open(f"level_{level + 1}.txt", "w") as file2:  # Open the text file that shall contain the game states of the next level
            print(f"Analyzing level {level + 1}...")  # Inform the user that the next level is in work
            player = level % 2  # The player who will make the next move (on level = 0, Player A (player = 0) makes the move on level + 1 = 1, and so on)
            apply_to_children(file1, file2, player)  # Apply moves to all children of the current level
            
        file1 = f"level_{level + 1}.txt"  # Update the file name for the next level

        with open("results.csv", "a") as f:  # Write the game statistics from the computed level to the CSV file
            print(f"{turns}, {level + 1}, {games}, {agency}, {awins}, {bwins}, {draws}, {timeouts}", file=f)
        # Inform the user that the level is completed, and print som of the statistics results
        print(f"Level {level + 1}: {games} games ({games/turns:.1%}), {turns} turns, agency: {agency/turns:.1%}")


if __name__ == "__main__":
    analyse_game_tree(17)  # Start the game analysis if this script is run directly