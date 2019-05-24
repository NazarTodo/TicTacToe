import copy

from board import Board, OutOfFieldError, CellIsOccupiedError


def game():
    """
    Function for playing tictactoe
    None -> None
    :return None
    """
    board = Board()

    while not board.game_is_over():
        user_move_row = int(
            input('Enter coordinates you want to put your figure(row)(0, 1, 2): '))
        user_move_col = int(
            input('Enter coordinates you want to put your figure(col)(0, 1, 2): '))
        try:
            board.move_is_possible((user_move_row, user_move_col))

            left_board = copy.deepcopy(board)
            right_board = copy.deepcopy(board)
            left_board.make_random_move()
            right_board.make_random_move()
            left_score = left_board.compute_score()
            right_score = right_board.compute_score()
            if right_score > left_score:
                board = right_board
            else:
                board = left_board

            print(board)

        except OutOfFieldError:
            print("The cell is out of range")
        except CellIsOccupiedError:
            print('The cell is not empty')

    print('The game is finished!\n')
    if board.game_is_over() == Board.DRAW:
        print('The friendship won')
    else:

        winner = 'User' if board.game_is_over() == Board.CROSS else 'Computer'
        print('The {} won'.format(winner))

    return


if __name__ == '__main__':
    game()
