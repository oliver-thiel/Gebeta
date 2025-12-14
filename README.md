# Gebeta
Gebeta is a traditional board game played in Ethiopia (Tesfamicael & Farsani, 2024). The Python code in this repository allows two players to play Gebeta in the terminal or one player to play against the computer. Furthermore, it includes code to analyse the Gebeta game tree.

## The Python code
The repository includes four Python files: `Gebeta_MCTS.py`, `Gebeta_game.py`, `Gebeta_analysis.py`, and `main.py`.  
The file `Gebeta_MCTS.py` requires [monte-carlo-tree-search 2.1.0 from PYPI](https://pypi.org/project/monte-carlo-tree-search/).

## Gebeta game
### Rules
Gebeta is a two-player, two-row mancala-style game with six pits in each row. The pits are called “homes”. Each player owns one row of homes. Forty-eight counters are evenly distributed into the twelve homes, with four counters in each home. A group of four counters is called a “family”.

Players pick up the counters from any of their homes and sow them in an anti-clockwise direction. In this context, “sowing” means distributing one counter at a time to adjacent homes. If the last counter lands in a home that is occupied, the player picks up the contents of this home and continues to sow. When the last counter lands in an empty home, the turn ends. When the last counter lands in a home that has three counters, it creates a family. The player captures the family by removing it and setting it aside. The turn ends. If, during sowing, a family is formed elsewhere, the owner of that home captures it.

The goal is to capture most families.

When all of a player's homes are empty, the player must pass, and the game ends. The opponent captures all remaining counters. The player with the most captured families wins the game.

### Playing Gebeta
You can start the game in the terminal by calling
```
python.exe Gebeta_MCTS.py
```
The program asks for the players' names. If a player has the name `Computer, the computer will make the moves for this player by applying a Monte Carlo Tree Search (MCTS) algorithm. Then the game starts and shows:
```diff
    Player A has 0 families.  
    Player B has 0 families.  
    Current board state:  
    B  |  4 |  4 |  4 |  4 |  4 |  4 |  
    A  |  4 |  4 |  4 |  4 |  4 |  4 |  
!   A  |  A |  B |  C |  D |  E |  F |  
    The following moves are made: []  
    The current player is A.  
    The next move is move number 1.  
    Player A's turn. Choose a home (A-F):  
```
It is Player A's turn to choose a home by entering a letter A, B, C, D, E, or F. After A has moved, e.g. by typing a<ENTER>, it is Player B's move. The board is shown from B's perspective.
```diff
    Player A has 0 families.  
    Player B has 0 families.  
    Current board state:  
    A  |  6 |  1 |  6 |  1 |  7 |  2 |  
    B  |  6 |  6 |  0 |  1 |  6 |  6 |  
!   B  |  F |  E |  D |  C |  B |  A |  
    The following moves are made: ['A1']  
    The current player is B.  
    The next move is move number 2.  
    Player B's turn. Choose a home (A-F):  
```
## Analysing the game
You can analyse the Gebeta game tree down to a depth of 18 levels by calling
```
python.exe Gebeta_analysis.py
```
The program will produce one text file for each level that contains all game states on this level.
[!Warning]
The file level_18.txt is 1.2 TB in size.

The game analysis will be written to the CSV-file `results.csv`. It will have the following content:
```
turns, level, games, agency, Awins, Bwins, draws, timeouts
6, 1, 0, 6, 0, 0, 0, 0
38, 2, 0, 38, 0, 0, 0, 0
178, 3, 0, 178, 0, 0, 0, 0
816, 4, 0, 812, 0, 0, 0, 0
3843, 5, 2, 3825, 2, 0, 0, 0
17641, 6, 4, 17557, 2, 1, 1, 0
76287, 7, 64, 75538, 29, 16, 19, 0
320100, 8, 255, 316053, 68, 92, 91, 4
1285021, 9, 1543, 1263422, 604, 379, 532, 28
4968533, 10, 5929, 4873254, 1246, 2735, 1831, 117
18617646, 11, 27580, 18211721, 10923, 7674, 8464, 519
67858391, 12, 107854, 66285252, 22818, 51415, 31230, 2391
242325708, 13, 419421, 236386601, 156833, 123219, 129700, 9669
850892297, 14, 1536244, 829395178, 328103, 719208, 451247, 37686
2949680649, 15, 5460769, 2874346165, 2057670, 1616802, 1645982, 140315
10128881536, 16, 19089095, 9869107371, 4191239, 8935572, 5463717, 498567
34520709817, 17, 63511777, 33653938583, 24032833, 19080036, 18691043, 1707865
117071728801, 18, 211552785, 114193683811, 47820057, 98415455, 59679406, 5637867
```
The columns are
- **turns**: The accumulated number of player moves, e.g. on level 1, Player A can make 6 different moves.
- **level**: The level number
- **games**: The accumulated number of finished games.
- **agency**: The agency measure is the proportion of turns for which the player to move has more than one legal move (Todd et al., 2025, p. 6).
- **Awins**: The accumulated number of games won by Player A.
- **Bwins**: The accumulated number of games won by Player B.
- **draws**: The accumulated number of games that end in a draw.
- **timeouts**: The accumulated number of games that are terminated by a timeout because they would lead to an infinite loop.

## Main function
You can start the program via
```
python.exe main.py
```
In this case, you can choose whether you want to play the game or analyse it. If you decide to analyse the game, you can select the depth you wish.

## References
- Todd, G., Padula, A. G., Stephenson, M., Piette, É., Soemers, D. J. N. J., & Togelius, J. (2025). *GAVEL: generating games via evolution and language models* [Conference Paper]. Proceedings of the 38th International Conference on Neural Information Processing Systems, Vancouver, BC, Canada. https://proceedings.neurips.cc/paper_files/paper/2024/file/c7b04e4e13bb77996d3ae2ff667231ac-Paper-Conference.pdf
- Tesfamicael, S. A., & Farsani, D. (2024). Creating a Culturally Responsive Mathematics Education: The Case of Gebeta Game in Ethiopia. In M. A. Ashraf & S. M. Tsegay (Eds.), *STEM Education - Recent Trends and New Advances.* IntechOpen. https://doi.org/10.5772/intechopen.114007
