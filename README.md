This project is divided in 3 different programs.

1/ npuzzle-gen.py generate puzzles of the size given as argument, the puzzle genereated might be solvable or unsolvable. '-s' option forces a solvable puzzle and '-u' option forces an unsolvable puzzle

2/ main.py solves the puzzle in the file given as argument using heuristic functions:
    - default or '-m' option: manhattan distance
    - '-H' option: hamming distance
    - 'l' option: manhattan distance with linear conflicts
    - '-M' option to have the list of moves instead of every state after each move

3/ game.py open a window with the puzzle in the file given as argument 
