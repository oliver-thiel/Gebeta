#Gebeta_game_np.py
#Gebeta game implementation using NumPy

import numpy as np

class Gebeta_game:
    """
    Gebeta is a traditional board game played in Ethiopia, similar to Mancala.
    This implementation simulates the game with two players, each having a row of 6 pits (called homes) and a store for the captured families.
    A family is a group of 4 seeds in a home.
    Players take turns to sow seeds from their homes, distributing them counter-clockwise.
    The game ends when one player has no seeds left in their homes, and the player with the most families in their store wins.
    """
    def __init__(self, status: np.array, moves: np.uint64):
        """
        Initialize the Gebeta game.

        Args:
            status (np.array): The initial game board status.
            moves (np.uint64): The sequence of moves made in the game.
        """
        self.players : list[str] = ["A", "B"]  # Player names
        self.board : np.array = status[:12]
        self.store : np.array = status[12:14]  # Store for each player
        self.player : np.uint8 = np.uint8(np.log10(moves) % 2)  # Determine current player based on the length of moves
        self.moves : np.uint64 = moves  # String to record moves


    def print_board(self):
        """
        Print the current game board and player information.
        """
        print(f"Player {self.players[0]} has {self.store[0]} families.")
        print(f"Player {self.players[1]} has {self.store[1]} families.")
        print("Current board state:")
        # Print the board in a more readable, aligned format
        print("| " + "| ".join(f"{x:2d} " for x in self.board[6:12]) + "|")  # Upper row (Player B)
        print("| " + "| ".join(f"{x:2d} " for x in self.board[:6]) + "|")  # Lower row (Player A)
        print(f"The following moves are made: {self.moves}")
        print(f"The current player is {self.players[self.player]}.")
        print(f"The next move is move number {np.uint8(np.log10(self.moves))}.")


    def sow(self, pit: np.uint8, row: np.uint8) -> bool:
        """
        Sows seeds from the specified pit in the specified row.

        Args:
            pit (np.uint8): The index of the pit to sow from (0-5).
            row (np.uint8): The row to sow from (0 for Player A, 1 for Player B).

        Returns:
            bool: True if the sowing was successful, False if the sowing does not end.
        """  
        for _ in range(50):
            seeds = self.board[pit + row * 6]  # Get the number of seeds in the specified pit
            if seeds == 0:
                return False  # Cannot sow from an empty pit
            self.board[pit + row * 6] = 0

            # Distributing seeds
            while seeds > 0:
                # We distribute counter-clockwise, i.e., to the right in the lower row and to the left in the upper row
                pit += 1 if row == 0 else -1
                if row == 0 and pit > 5:  # Switch to the last pit in the upper row
                    row = 1
                    pit = 5
                elif row == 1 and pit < 0:  # Switch to the first pit in the lower row
                    row = 0
                    pit = 0

                self.board[pit + row * 6] += 1
                seeds -= 1
                if self.board[pit + row * 6] == 4:
                    self.board[pit + row * 6] = 0  # Empty the pit if it reaches 4
                    if seeds == 0: # If the last seed lands in a pit with 4 seeds, it counts for the player
                        self.store[self.player] += 1
                        return True
                    # If the pit reaches 4 seeds during distribution, it counts for the player who owns that row
                    self.store[row] += 1

            if self.board[pit + row * 6] == 1:
                return True # If the last seed lands in an empty pit, the player's turn ends

            # Otherwise, continue sowing from the current pit (for-loop will continue)
            
        return False  # Too many iterations, break out of the sowing loop


    def move(self, pit: int) -> bool:
        """
        Make a move in the game.

        Args:
            pit (int): The index of the pit to move from (0-5).

        Returns:
            bool: True if the game continues, False if the game ends.
        """
        if self.sow(pit, self.player):
            self.moves = self.moves * 10 + pit  # Append the move to the "moves string"
        else:
            self.moves = self.moves * 10 + 9  # Mark the move as too long if it cannot be made 
            return False  # Invalid move, because of timeout

        # Check for winner
        if winner := self.check_winner():
            self.moves = self.moves * 10 + winner
            return False
        
        # Switch player
        self.player = 1 - self.player
        return True


    def make_move(self) -> int:
        """
        Make a move for the current player by selecting a home.
        The player is prompted to choose a home with seeds.
        If the selected home is empty, the player is prompted to choose a different home.

        Returns:
            int: The home if the move was successful.
        """
        while True:
            print(f"Player {self.players[self.player]}'s turn. Choose a home (0-5):")
            home = int(input())
            if 0 <= home < 6 and self.board[home + 6 * self.player] > 0:
                return home
            else:
                print(f"Invalid move: Player {self.players[self.player]} cannot move from home {home}.")
                print("Please choose a different home.")


    def check_winner(self) -> int:
        """
        Check if there is a winner.
        If one player has no seeds left in their homes, the player with the most captured families is the winner.
        
        Returns:
            str: the winner's name or 'D' for a draw or an empty string if the game is still ongoing.
        """
        if max(self.board[:6]) == 0 or max(self.board[6:]) == 0:
            if self.store[0] > self.store[1]:  # Player A wins
                return 6
            elif self.store[1] > self.store[0]:  # Player B wins
                return 7
            else:  # Draw
                return 8
        return 0  # Game is still ongoing

    def print_end(self):
        """
        Print the final board state and the winner.
        """
        print("Game over!")
        print(f"Player {self.players[0]} has {self.store[0]} families.")
        print(f"Player {self.players[1]} has {self.store[1]} families.")
        print("Current board state:")
        # Print the board in a more readable, aligned format
        print("| " + "| ".join(f"{x:2d} " for x in self.board[6:]) + "|")  # Upper row (Player B)
        print("| " + "| ".join(f"{x:2d} " for x in self.board[:6]) + "|")  # Lower row (Player A)
        print(f"The following moves are made: {self.moves}")
        winner : int = int(self.moves % 10 - 6)  # Get the last digit to determine the game outcome
        print(f"The winner is {self.players[winner]}." if winner != 2 else "The game is a draw.")


def play_game():
    """
    Two players can play Gebeta in the terminal until there is a winner or a draw.
    """
    # Initial game state: two rows of homes and a store for each player
    initial_status : np.array = np.array([4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0], dtype=np.int8)
    moves : np.uint64 = 9  # Record of moves made

    # Create a new game instance with the initial status and moves
    game = Gebeta_game(initial_status, moves)

    # Start the game loop
    playing : bool = True
    while playing:
        game.print_board()
        pit = game.make_move()
        playing = game.move(pit)
        if not playing:
            game.print_end()
