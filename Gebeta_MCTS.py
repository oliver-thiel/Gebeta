#Gebeta_MCTS.py
#Gebeta game implementation with Monte Carlo Tree Search

from copy import deepcopy

from mcts.base.base import BaseState, BaseAction
from mcts.searcher.mcts import MCTS


class GebetaGameState(BaseState):
    """
    Gebeta is a traditional board game played in Ethiopia, similar to Mancala.
    This implementation simulates the game with two players, each having a row of 6 pits (called homes) and a store for the captured families.
    A family is a group of 4 seeds in a home.
    Players take turns to sow seeds from their homes, distributing them counter-clockwise.
    The game ends when one player has no seeds left in their homes, and the player with the most families in their store wins.
    """
    def __init__(self) -> None:
        """
        Initialize the Gebeta game.
        """
        # The game board is a list of 14 integers representing the 12 homes A1,..., F1, F2,..., A2 and the 2 stores SA and SB
        self.board : list[int] = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0]  # Initially, each home contains four seeds
        # Each home can be addressed in three different ways:
        # 1. pit    = the index in the list self.board, i.e., 0,..., 11
        # 2. home   = the label A, B, C, D, E, or F of the home, e.g., home C = pit 2 for Player A and pit 9 for Player B
        # 3. move   = the index of the home label in the string "ABCDEF"

        # Each player can be addressed in three different ways
        # 1. playerindex    = the index of the current player (0 for Player A, 1 for Player B)
        self.playerindex : int = 0
        # 2. playername     = the name of the current player in the list self.names
        self.names : list[str] = ['A', 'B']  # The initial players' names are 'A' and 'B'. They can be changed
        # 3. playerlabel    = 1 for the maximising player and -1 for the minimising player as used by the MCTS algorithm
        self.maximising : int = 0  # Index of the player who is maximising (i.e. the Computer or player A if both players are human)

        # The moves are recorded in a list of strings
        self.moves : list[str] = []


    # Auxiliary functions
    def home_to_move(self, home: str) -> int:
        """
        Converts the label A, B, C, D, E, or F of a home into the index of the home label in the string "ABCDEF"

        Args:
            home (str): the label A, B, C, D, E, or F of a home

        Returns:
            int: the index of the home label in the string "ABCDEF"
        """
        return ord(home) - ord('A')
    

    def home_to_pit(self, home: str) -> int:
        """
        Converts the label A, B, C, D, E, or F of a home into the index of the pit

        Args:
            home (str): the label A, B, C, D, E, or F of a home

        Returns:
            int: the index of the pit, e.g., home C = pit 2 for Player A and pit 9 for Player B
        """
        return (((-1)**self.playerindex) * self.home_to_move(home)) + (11 * self.playerindex)
    

    def move_to_pit(self, move: int) -> int:
        """
        Converts the index of a move (0,..., 5) into the index of the pit (0,..., 11)

        Args:
            move (int): the index of a move (0,..., 5)

        Returns:
            int: the index of the pit, e.g., move 2 = pit 2 for Player A and pit 9 for Player B
        """
        return (((-1)**self.playerindex) * move) + (11 * self.playerindex)
    

    def move_to_home(self, move: int) -> str:
        """
        Converts the index of a move (0,..., 5) into the label of the home (A1,..., F1, F2,..., A2)

        Args:
            move (int): the index of a move (0,..., 5)

        Returns:
            str: the label of the home (A1,..., F1, F2,..., A2)
        """
        homes = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'F2', 'E2', 'D2', 'C2', 'B2', 'A2']
        return homes[self.move_to_pit(move)]
    

    def pit_not_empty(self, home: str) -> bool:
        """
        Checks if the pit with the label home is not empty

        Args:
            home (str): the label A, B, C, D, E, or F of a home

        Returns:
            bool: True if the pit is empty
        """
        return self.board[self.home_to_pit(home)] > 0
    

    # GUI functions
    def print_board(self):
        """
        Print the current game board and player information.
        """
        print(f"Player {self.names[0]} has {self.board[12]} families.")
        print(f"Player {self.names[1]} has {self.board[13]} families.")
        print("Current board state:")
        # Print the board in a more readable, aligned format
        if self.playerindex == 0:
            print(f"{self.names[1]:<12}| " + "| ".join(f"{x:2d} " for x in self.board[6:12][::-1]) + "|")  # Upper row (Player B)
            print(f"{self.names[0]:<12}| " + "| ".join(f"{x:2d} " for x in self.board[:6]) + "|")  # Lower row (Player A)
            print(f"\033[1;37;40m{self.names[0]:<12}|  A |  B |  C |  D |  E |  F |\033[0m")  # Lower row header
        else:
            print(f"{self.names[0]:<12}| " + "| ".join(f"{x:2d} " for x in self.board[:6][::-1]) + "|")  # Upper row (Player A)
            print(f"{self.names[1]:<12}| " + "| ".join(f"{x:2d} " for x in self.board[6:12]) + "|")  # Upper row (Player B)
            print(f"\033[1;37;40m{self.names[1]:<12}|  F |  E |  D |  C |  B |  A |\033[0m")  # Lower row header
        print(f"The following moves are made: {self.moves}")
        print(f"The current player is {self.names[self.playerindex]}.")
        print(f"The next move is move number {len(self.moves) + 1}.")


    def make_move(self) -> 'Action':
        """
        Make a move for the current human player by selecting a home.
        The player is prompted to choose a home with seeds.
        If the selected home is empty, the player is prompted to choose a different home.

        Returns:
            Action: The action taken by the player.
        """
        while True:
            print(f"Player {self.names[self.playerindex]}'s turn. Choose a home (A-F):")
            home = input().upper()
            if home in "ABCDEF":
                if self.pit_not_empty(home):
                    return Action(self.home_to_move(home))
            else:
                print(f"\033[1;31mInvalid move: Player {self.names[self.playerindex]} cannot move from home {home}.\033[0m")
                print("Please choose a different home.")


    def print_end(self):
        """
        Print the final board state and the winner.
        """
        print("\033[1;31mGame over!\033[0m")
        print(f"Player {self.names[0]} has {self.board[12]} families.")
        print(f"Player {self.names[1]} has {self.board[13]} families.")
        print(f"The following moves are made: {self.moves}")
        match self.moves[-1]:  # Get the last character to determine the game outcome
            case "A": # Player A wins
                print(f"\033[1;31mThe winner is {self.names[0]}.\033[0m")
            case "B": # Player B wins
                print(f"\033[1;31mThe winner is {self.names[1]}.\033[0m")
            case "D": # Draw
                print("The game is a draw.")
            case "T": # Timeout due to an infinite loop
                print("The game ended due to a timeout (infinite loop). No winner.")
            case _:  # Fallback case
                print("The game ended unexpectedly. No winner.")


    # Game mechanics
    def sow(self, pit: int) -> bool:
        """
        Sows seeds from the specified pit.

        Args:
            pit (int): The index of the pit to sow from (0-11).

        Returns:
            bool: True if the sowing was successful, False if the sowing does not end.
        """  
        for _ in range(50):  # Limit the number of iterations to prevent infinite loops
            seeds = self.board[pit]  # Get the number of seeds in the specified pit
            if seeds == 0:
                return False  # Cannot sow from an empty pit
            self.board[pit] = 0

            # Distributing seeds
            while seeds > 0:
                # We distribute counter-clockwise, i.e., to the right in the lower row (and to the left in the upper row)
                pit += 1
                if pit == 12:  # Reset to the beginning after reaching the end of the board
                    pit = 0
                self.board[pit] += 1  # Place one seed in the next pit
                seeds -= 1  # Decrease the number of seeds to distribute
                if self.board[pit] == 4:  # Check if the pit reaches 4 seeds, i.e., a family
                    self.board[pit] = 0  # Empty the pit if it reaches 4 seeds
                    if seeds == 0: # If the last seed lands in a pit with 4 seeds, it counts for the player
                        self.board[12 + self.playerindex] += 1
                        return True
                    # If the pit reaches 4 seeds during distribution, it counts for the player who owns that row
                    row = 0 if pit < 6 else 1
                    self.board[12 + row] += 1

            if self.board[pit] == 1:    # If the last seed lands in an empty pit,
                return True             # the player's turn ends

            # Otherwise, continue sowing from the current pit (for-loop will continue)
            
        return False  # Too many iterations, break out of the sowing loop


    def check_winner(self, player: int) -> str:
        """
        Check if there is a winner.
        If the other player has no seeds left in their homes, the player with the most captured families is the winner.
        
        Returns:
            str: the winner's name or 'D' for a draw or an empty string if the game is still ongoing.
        """
        other_player = 1 - player
        if max(self.board[other_player * 6:other_player * 6 + 6]) == 0:
            rest = sum(self.board[player * 6:player * 6 + 6])  # Count remaining seeds in the player's homes
            self.board[12 + player] += rest // 4  # Add remaining families to the player's store
            if self.board[12] > self.board[13]:  # Player A wins
                return "A"
            elif self.board[13] > self.board[12]:  # Player B wins
                return "B"
            else:  # Draw
                return "D"
        return ""  # Game is still ongoing


    # Functions required by the MCTS algorithm
    def get_possible_actions(self) -> list['Action']:
        """
        Returns an iterable of all actions which can be taken from this state.
        """
        actions : list['Action'] = []  # List of possible moves
        for move in range(6):  # Try all possible moves
            if self.board[self.move_to_pit(move)] != 0:  # The pit is not empty
                actions.append(Action(move))
        return actions


    def take_action(self, action: 'Action') -> 'GebetaGameState':
        """
        Makes a move in the game (for both computer and human players).

        Args:
            action (Action): A representation of the action taken by a player.

        Returns:
            GebetaGameState: Returns the game state which results from taking action.
        """
        newState = deepcopy(self)
        if newState.sow(self.move_to_pit(action.move)):
            newState.moves.append(self.move_to_home(action.move))   # Record the move
        else:
            newState.moves.append('T')  # Mark the move as timeout if it ended in an infinite loop 
            return newState  # The game ends, because of timeout

        # Check for winner
        if winner := newState.check_winner(newState.playerindex):
            newState.moves.append(winner)
            return newState # The game ends with a winner or a draw
        
        # Switch player
        newState.playerindex = 1 - newState.playerindex
        return newState # The game continues
    

    def is_terminal(self) -> bool:
        """
        Returns True if this state is a terminal state

        Returns:
            bool: True if this state is a terminal state
        """
        if len(self.moves) > 4:
            return self.moves[-1] in ['A', 'B', 'D', 'T']
        return False
    

    def get_reward(self) -> float:
        """
        Returns the reward for this state. Only needed for terminal states.

        Returns:
            float: The number for families captured by the computer minus the number of families captured by the human player
        """
        return self.board[12 + self.maximising] - self.board[13 - self.maximising]  # Return score
    

    def get_current_player(self) -> int:
        """
        Returns 1 if it is the computer player's turn to choose an action, or -1 for the human player

        Returns:
            int: 1 if it is the computer player's turn to choose an action, or -1 for the human player
        """
        return 1 if self.playerindex == self.maximising else -1


class Action(BaseAction):
    """Action representing a move in the Gebeta game."""

    def __init__(self, move: int) -> None:
        """
        Creates a representation of a move in the Gebeta game

        Args:
            move (int): The index of the chosen move: 0-5 for the homes A-F
        """
        self.move = move


    def __str__(self) -> str:
        """Converts the index into a letter

        Returns:
            str: The letter of the chosen home: A-F
        """
        homes = "ABCDEF"
        return homes[self.move]


    def __repr__(self) -> str:
        return str(self)


    def __eq__(self, other: object) -> bool:
        return self.__class__ == other.__class__ and self.move == other.move


    def __hash__(self) -> int:
        return self.move


def play_game():
    """
    Two players can play Gebeta in the terminal until there is a winner or a draw. One player can be a computer.
    1. The game starts with each home containing 4 seeds.
    2. Players take turns to sow seeds from their homes.
    3. The game ends when one player has no seeds left in their homes. The player with the most families in their store wins.
    Players can enter their names or choose to play against the computer.
    The game board is displayed after each move, showing the current state and the moves made so far.
    The game announces the winner or if the game ends in a draw.
    The game can handle invalid moves and prompts players to choose valid homes.
    The computer player uses a Monte Carlo Tree Search (MCTS) to choose its moves.
    The game provides clear instructions and feedback to players throughout the game.
    The game can end due to a timeout if a player enters an infinite loop of moves.
    The game is played in the terminal, making it accessible and easy to use.
    The game uses colored text to enhance the user experience and highlight important information.
    The game is implemented in Python, making it easy to modify and extend.
    The game is designed to be fun and engaging for players of all skill levels
    """
    # Create a new game instance with the initial status and moves
    game = GebetaGameState() 
    searcher = MCTS(time_limit=1500)

    # choose players
    computer_comment = ". (Enter 'Computer' for computer player.)"
    name = input(f"Enter the name of Player A{computer_comment}: ")
    game.names[0] = name if name else "A"
    if game.names[0] == "Computer":
        computer_comment = ""  # No need to prompt for Player B if Player A is the computer
    name = input(f"Enter the name of Player B{computer_comment}: ")
    while name == game.names[0]:
        print("Player B cannot have the same name as Player A. Please choose a different name.")
        name = input(f"Enter the name of Player B{computer_comment}: ")
    game.names[1] = name if name else "B"
    if game.names[1] == "Computer":
        game.maximising = 1

    # Start the game loop
    while True:
        game.print_board()  # Print the current board state
        if game.names[game.playerindex] == 'Computer':
            action = searcher.search(initial_state=game)  # Get the computer's move
        else:
            action = game.make_move()  # Get the human player's move
        game = game.take_action(action)  # Make the move
        if game.is_terminal():  # The game has ended, either with a winner or a draw
            game.print_end()  # Print the final board state and the winner
            break  # Break out of the while loop


if __name__ == "__main__":
    play_game()
