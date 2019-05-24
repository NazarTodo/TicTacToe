# Partly made by Oles Dobosevych

import copy
import random
from tictactoe.btree import Tree
from tictactoe.btnode import Node


class OutOfFieldError(BaseException):
    pass


class CellIsOccupiedError(BaseException):
    pass


def generate_winning_combinations():
    combinations = []
    for i in range(3):
        combination1 = []
        combination2 = []
        for j in range(3):
            combination1.append((i, j))
            combination2.append((j, i))
        combinations.append(combination1)
        combinations.append(combination2)

    combinations.append([(0, 0), (1, 1), (2, 2)])
    combinations.append([(0, 2), (1, 1), (2, 0)])
    return combinations


class Board:
    NOUGHT = 1
    CROSS = -1
    EMPTY = 0

    NOUGHT_WINNER = 1
    CROSS_WINNER = -1
    DRAW = 2
    NOT_FINISHED = 0

    WINNING_COMBINATIONS = generate_winning_combinations()

    def __init__(self):
        self._field = [[0] * 3 for _ in range(3)]
        self.previous = Board.NOUGHT
        self._moves_num = 0

    def move_is_possible(self, cell):
        if cell[0] >= 3 or cell[0] >= 3 or cell[0] < 0 or cell[1] < 0:
            raise OutOfFieldError("The cell is out of range")
        if self._field[cell[0]][cell[1]] != 0:
            raise CellIsOccupiedError('The cell is not empty')
        self.previous = -self.previous
        self._field[cell[0]][cell[1]] = self.previous
        self._moves_num += 1
        return True

    def game_is_over(self):
        for combination in self.WINNING_COMBINATIONS:
            lst = []
            for cell in combination:
                lst.append(self._field[cell[0]][cell[1]])
            if max(lst) == min(lst) and max(lst) != Board.EMPTY:
                return max(lst)
        if self._moves_num == 9:
            return Board.DRAW

        return Board.NOT_FINISHED

    def make_random_move(self):
        possible_moves = []
        for i in range(3):
            for j in range(3):
                if self._field[i][j] == Board.EMPTY:
                    possible_moves.append((i, j))
        cell = random.choice(possible_moves)
        self.previous = -self.previous
        self._field[cell[0]][cell[1]] = self.previous
        self._moves_num += 1
        return True

    def compute_score(self):
        game_over = self.game_is_over()
        if game_over:
            winner_scores = {Board.NOUGHT_WINNER: 1, Board.CROSS_WINNER: -1,
                             Board.DRAW: 0}
            return winner_scores[game_over]
        n1 = Node(self)
        board = Tree()
        board.root = n1
        left_board = copy.deepcopy(self)
        right_board = copy.deepcopy(self)
        left_move = left_board.make_random_move()
        right_move = right_board.make_random_move()
        board.root.left = Node(left_move)
        board.root.right = Node(right_move)
        return left_board.compute_score() + right_board.compute_score()

    def __str__(self):
        to_return = ''
        for row in self._field:
            for i in row:
                to_return += ' '
                if i == 0:
                    to_return += ' '
                elif i == 1:
                    to_return += 'O'
                else:
                    to_return += 'X'
            to_return += '\n'

        return to_return

