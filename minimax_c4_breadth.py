import connect_four
import pprint

ROWS = 5
COLUMNS = 3
TO_WIN = 3

MAX = 1
MIN = 2

BLANK_BOARD = [[0 for i in range(COLUMNS)] for j in range(ROWS)]

def is_row_win(grid):
    mr = (COLUMNS + 1)/2
    for row in reversed(grid):
        streak = 0
        if row[mr] != 0:
            is_winner = row[mr]
            for column in row:
                if column == is_winner:
                    streak += 1
                else:
                    streak = 0
                if streak >= TO_WIN:
                    return is_winner
    return None

def is_col_win(grid):
    mc = grid[((ROWS+1)/2)]
    for i in range(COLUMNS):
        #check to see if row3 and 4 have a match first
        if mc[i] != 0:
            is_winner = mc[i]
            streak = 0
            for row in reversed(grid):
                if row[i] == is_winner:
                    streak += 1
                else:
                    streak = 0
                if streak >= TO_WIN:
                    return is_winner
    return None

def check_diagonal(player, index, grid):
    f_index = index
    b_index = index
    f_streak = 1
    b_streak = 1

    for row in reversed(grid):
        f_index += 1
        b_index -= 1
        if f_index < COLUMNS and row[f_index] == player:
            f_streak += 1
        else:
            f_streak = 0
        if b_index >= 0 and row[b_index] == player:
            b_streak += 1
        else:
            b_streak = 0
        if f_streak == 0 and b_streak == 0:
            return None
    if f_streak == TO_WIN or b_streak == TO_WIN:
        return player
    else:
        return None

def is_diag_win(grid):
    mr = (ROWS + 1)/2
    for i, row in enumerate(reversed(grid[mr:])):
        for j, column in enumerate(row):
            if column != 0:
                top = ROWS - TO_WIN - i
                bottom = ROWS - 1 - i
                winner = check_diagonal(column, j,  grid[top:bottom])
                if winner:
                    return winner
    return None

def determine_winner(grid):
    return is_row_win(grid) or is_col_win(grid) or is_diag_win(grid)

def make_sample_board(b):
    r = ROWS
    b[connect_four.get_row(b,1,ROWS)][1] = MAX
    b[connect_four.get_row(b,0,ROWS)][0] = MIN
    b[connect_four.get_row(b,1,ROWS)][1] = MAX
    b[connect_four.get_row(b,1,ROWS)][1] = MIN
    return b

def add_player_to_board(b, player):
    boards = []
    for i in range(COLUMNS):
        new_b = [row[:] for row in b]
        row = connect_four.get_row(b, i, ROWS)
        if row != None:
            new_b[connect_four.get_row(b, i, ROWS)][i] = player
            boards.append(new_b[:])
    return boards

def is_board(board):
    for row in board:
        for column in row:
            if type(column) == type(0):
                return True
    return False

def recur_add_player(boards, player):
    if is_board(boards):
        if determine_winner(boards):
            return None
        else:
            return add_player_to_board(boards, player)
    else:
        all_the_boards = []
        for b in boards:
            next_iter_boards = recur_add_player(b, player)
            if next_iter_boards:
                all_the_boards.append(next_iter_boards[:])
        return all_the_boards



def test_max(board, num):
    print
    print "MAX", num
    max_1 = recur_add_player(board, MAX)
    for item in max_1:
        pp.pprint(item)
        print
    return max_1

def test_min(board, num):
    print
    print "MIN", num
    min_1 = recur_add_player(board, MIN)
    for item in min_1:
        pp.pprint(item)
        print
    return min_1

max_1_SOLUTION = [
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [0, 1, 0], [2, 1, 1]]]


min_1_SOLUTION = [
    [[[0, 0, 0], [0, 0, 0], [2, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 2, 0], [0, 2, 0], [1, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 0], [2, 1, 2]]],

    [[[0, 0, 0], [0, 1, 0], [0, 2, 0], [2, 1, 0], [2, 1, 0]],
     [[0, 2, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 0]],
     [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 1, 0], [2, 1, 2]]],

    [[[0, 0, 0], [0, 0, 0], [0, 2, 0], [2, 1, 0], [2, 1, 1]],
     [[0, 0, 0], [0, 2, 0], [0, 2, 0], [0, 1, 0], [2, 1, 1]],
     [[0, 0, 0], [0, 0, 0], [0, 2, 0], [0, 1, 2], [2, 1, 1]]]]

row_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [0, 2, 0], [1, 1, 1], [2, 1, 2]]
col_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [2, 1, 0]]
diag_win_EXAMPLE = [[0, 0, 0], [0, 0, 0], [1, 2, 0], [2, 1, 0], [2, 1, 1]]

def play_board(board, depth):
    for i in range(depth):
        max_board = recur_add_player(board, MAX)
        min_board = recur_add_player(max_board, MIN)
        board = min_board
    return board

def print_board(board, depth):
    boards = play_board(board, depth)
    for board_set in boards:
        pprint.pprint(board_set)


def is_stable_board(board, i):
    prev_level = play_board(board, i-1)
    cur_level = play_board(board, i)
    return prev_level == cur_level

def find_level(board):
    #before accounting for wins, board stabilizes at 6th round.
    if is_stable_board(board, ROWS+1):
        return None



if __name__ == '__main__':
    board = make_sample_board(BLANK_BOARD)
    pp = pprint.PrettyPrinter(width = 40)
    #pp.pprint(board)

    first_level = play_board(board, 1)
    print_board(board, 5)

    assert first_level == min_1_SOLUTION
    assert is_row_win(row_win_EXAMPLE) == True
    assert is_col_win(col_win_EXAMPLE) == True
    assert is_diag_win(diag_win_EXAMPLE) == True