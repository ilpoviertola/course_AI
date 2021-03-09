"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_amount = 0
    o_amount = 0

    for row in board:
        for box in row:
            if box is X:
                x_amount += 1
            elif box is O:
                o_amount += 1

    return X if x_amount <= o_amount else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    allowed_actions = set()
    row_num = 0

    for row in board:
        col_num = 0
        for box in row:
            if box is EMPTY:
                allowed_actions.add((row_num, col_num))
            col_num += 1
        row_num += 1

    return allowed_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tmp_board = copy.deepcopy(board)

    if action not in actions(board):
        raise Exception("Action is not allowed!")

    else:
        tmp_board[action[0]][action[1]] = player(board)
        return tmp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for mark in X, O:
        col_num = 0
        diagonals_checked = False
        for row in board:
            # Horizontal check
            if all(box is mark for box in row):
                return mark
            # Vertical check
            elif all(box is mark for box in get_column(board, col_num)):
                return mark
            # Diagonal check (necessary only once per mark)
            elif not diagonals_checked:
                from_top_left, from_top_right = get_diagonals(board)
                if all(box is mark for box in from_top_left):
                    return mark
                elif all(box is mark for box in from_top_right):
                    return mark
                diagonals_checked = True

            col_num += 1

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if all(all(box is not EMPTY for box in row) for row in board):
        return True

    elif winner(board) is X or winner(board) is O:
        return True

    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1

    elif winner(board) is O:
        return -1

    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Or None if the board is terminal.
    """
    return exec_minimax_alphabeta(board, float('-inf'), float('inf'))[0]


def exec_minimax_alphabeta(board, alpha, beta):
    """
    Returns list containing best move and its utility score.
    """

    if terminal(board) is True:
        return [None, utility(board)]

    # Next agent is max
    if player(board) is X:
        return max_value(board, alpha, beta)

    # Next agent is min
    else:
        return min_value(board, alpha, beta)


def max_value(board, alpha, beta):
    """
    Maximum utility values for available moves. Returns best value and
    action as a list.
    """
    best_action_score = [None, -2]

    for action in actions(board):
        board_tmp = result(board, action)
        cur_action_score = exec_minimax_alphabeta(board_tmp, alpha, beta)
        cur_action_score[0] = action

        if cur_action_score[1] > best_action_score[1]:
            best_action_score = cur_action_score

        if best_action_score[1] >= beta:
            return best_action_score

        if best_action_score[1] > alpha:
            alpha = best_action_score[1]

    return best_action_score


def min_value(board, alpha, beta):
    """
    Minimum utility values for available moves. Returns best value and
    action as a list.
    """
    best_action_score = [None, 2]
    for action in actions(board):
        board_tmp = result(board, action)
        cur_action_score = exec_minimax_alphabeta(board_tmp, alpha, beta)
        cur_action_score[0] = action

        if cur_action_score[1] < best_action_score[1]:
            best_action_score = cur_action_score

        if best_action_score[1] <= alpha:
            return best_action_score

        if best_action_score[1] < beta:
            beta = best_action_score[1]

    return best_action_score


def get_column(board, col_num):
    """
    Returns requested column from board as a list.
    """
    column = []

    for row in board:
        column.append(row[col_num])

    return column


def get_diagonals(board):
    """
    Returns diagonals of the board as lists.
    """
    from_top_left = [
        board[0][0], board[1][1], board[2][2]
    ]
    from_top_right = [
        board[0][2], board[1][1], board[2][0]
    ]

    return from_top_left, from_top_right
