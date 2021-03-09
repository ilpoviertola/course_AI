from tictactoe import player
from tictactoe import actions
from tictactoe import result
from tictactoe import winner
from tictactoe import terminal
from tictactoe import utility

X = "X"
O = "O"
EMPTY = None

board = [[X, X, O],
         [O, O, O],
         [X, X, EMPTY]]

print(utility(board))
