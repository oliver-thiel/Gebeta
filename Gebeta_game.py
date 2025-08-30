#Gebeta_game.py
#Gebeta game implementation

class Gebeta_game:
    """
    Gebeta is a traditional board game played in Ethiopia, similar to Mancala.
    This implementation simulates the game with two players, each having a row of 6 pits (called homes) and a store for the captured families.
    A family is a group of 4 seeds in a home.
    Players take turns to sow seeds from their homes, distributing them counter-clockwise.
    The game ends when one player has no seeds left in their homes, and the player with the most families in their store wins.
    """
    def __init__(self, status: list[int], player: int):
        """
        Initialize the Gebeta game.

        Args:
            status (list[int]): The initial game board status.
            player (int): The current player (0 for Player A, 1 for Player B).
        """
        self.players : list[str] = ["A", "B"]  # Player names
        self.board : list[int] = status  # The game board, a list of 14 integers representing the homes and stores
        self.player : int = player  # Current player (0 for Player A, 1 for Player B)
        self.moves : str = "S"  # Record of moves made
        self.variant : bool = True  # Whether to use the variant rule (counting remaining seeds in homes)


    def print_board(self):
        """
        Print the current game board and player information.
        """
        print(f"Player {self.players[0]} has {self.board[12]} families.")
        print(f"Player {self.players[1]} has {self.board[13]} families.")
        print("Current board state:")
        # Print the board in a more readable, aligned format
        if self.player == 0:
            print("B  | " + "| ".join(f"{x:2d} " for x in self.board[6:12][::-1]) + "|")  # Upper row (Player B)
            print("A  | " + "| ".join(f"{x:2d} " for x in self.board[:6]) + "|")  # Lower row (Player A)
            print("\033[1;37;40mA  |  0 |  1 |  2 |  3 |  4 |  5 |\033[0m")  # Lower row header
        else:
            print("A  | " + "| ".join(f"{x:2d} " for x in self.board[:6][::-1]) + "|")  # Upper row (Player A)
            print("B  | " + "| ".join(f"{x:2d} " for x in self.board[6:12]) + "|")  # Upper row (Player B)
            print("\033[1;37;40mB  |  5 |  4 |  3 |  2 |  1 |  0 |\033[0m")  # Lower row header
        print(f"The following moves are made: {self.moves}")
        print(f"The current player is {self.players[self.player]}.")
        print(f"The next move is move number {len(self.moves)}.")


    def sow(self, pit: int, row: int) -> bool:
        """
        Sows seeds from the specified pit in the specified row.

        Args:
            pit (int): The index of the pit to sow from (0-5).
            row (int): The row to sow from (0 for Player A, 1 for Player B).

        Returns:
            bool: True if the sowing was successful, False if the sowing does not end.
        """  
        for _ in range(50):
            home = pit + row * 6  # Calculate the home index based on the row
            seeds = self.board[home]  # Get the number of seeds in the specified pit
            if seeds == 0:
                return False  # Cannot sow from an empty pit
            self.board[home] = 0

            # Distributing seeds
            while seeds > 0:
                # We distribute counter-clockwise, i.e., to the right in the lower row and to the left in the upper row
                pit += 1
                if pit == 6:  # Switch to the other row after the last pit in the row
                    row = 1 - row
                    pit = 0
                home = pit + row * 6  # Update the home index based on the new row
                self.board[home] += 1  # Place one seed in the next pit
                seeds -= 1  # Decrease the number of seeds to distribute
                if self.board[home] == 4:
                    self.board[home] = 0  # Empty the pit if it reaches 4
                    if seeds == 0: # If the last seed lands in a pit with 4 seeds, it counts for the player
                        self.board[12 + self.player] += 1
                        return True
                    # If the pit reaches 4 seeds during distribution, it counts for the player who owns that row
                    self.board[12 + row] += 1

            if self.board[home] == 1:
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
            self.moves += f"{pit}" if self.player == 0 else f"{5 - pit}"  # Record the move
        else:
            self.moves += "T"  # Mark the move as timeout if it ended in an infinite loop 
            return False  # The game ends, because of timeout

        # Check for winner
        if winner := self.check_winner(self.player):
            self.moves += winner
            return False # The game ends with a winner or a draw
        
        # Switch player
        self.player = 1 - self.player
        return True # The game continues


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
            pit = int(input())
            if 0 <= pit < 6:
                if self.player == 1:
                    pit = 5 - pit  # Adjust for Player B's homes
                if self.board[pit + self.player * 6] > 0:
                    return pit
            else:
                print(f"\033[1;31mInvalid move: Player {self.players[self.player]} cannot move from home {pit}.\033[0m")
                print("Please choose a different home.")


    def check_winner(self, player: int) -> str:
        """
        Check if there is a winner.
        If the other player has no seeds left in their homes, the player with the most captured families is the winner.
        
        Returns:
            str: the winner's name or 'D' for a draw or an empty string if the game is still ongoing.
        """
        other_player = 1 - player
        if max(self.board[other_player * 6:other_player * 6 + 6]) == 0:
            if self.variant:
                rest = sum(self.board[player * 6:player * 6 + 6])  # Count remaining seeds in the player's homes
                self.board[12 + player] += rest // 4  # Add remaining seeds to the player's store
            if self.board[12] > self.board[13]:  # Player A wins
                return self.players[0]
            elif self.board[13] > self.board[12]:  # Player B wins
                return self.players[1]
            else:  # Draw
                return "D"
        return ""  # Game is still ongoing


    def print_end(self):
        """
        Print the final board state and the winner.
        """
        print("\033[1;31mGame over!\033[0m")
        print(f"Player {self.players[0]} has {self.board[12]} families.")
        print(f"Player {self.players[1]} has {self.board[13]} families.")
        print(f"The following moves are made: {self.moves}")
        winner : str = self.moves[-1]  # Get the last character to determine the game outcome
        print(f"\033[1;31mThe winner is {winner}.\033[0m" if winner != "D" else "The game is a draw.")


def play_game():
    """
    Two players can play Gebeta in the terminal until there is a winner or a draw.
    """
    # Initial game state: two rows of homes and a store for each player
    initial_status = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0]

    # Create a new game instance with the initial status and moves
    game = Gebeta_game(initial_status, 0)  # Start with Player A

    # Start the game loop
    playing : bool = True
    while playing:
        game.print_board()  # Print the current board state
        pit = game.make_move()  # Get the player's move
        playing = game.move(pit)  # Make the move and check if the game continues
        if not playing:  # The game has ended, either with a winner or a draw
            game.print_end()  # Print the final board state and the winner


if __name__ == "__main__":
    play_game()
