from typing import List
from bingo_ui import show_banana_bingo, show_bingo_row, show_bingo_diagonal, show_bingo_column


class Score:
    def __init__(self, size: int):
        self.size = size
        self.values = [[0] * size for _ in range(size)]
        self.selection = [[False] * size for _ in range(size)]
        self.row_selection = [0] * size
        self.col_selection = [0] * size
        self.dia_selection = [0] * 2
        self.score = 0
        self.bingos = 1
        self.board = []

    def set_board(self, board):
        self.board = board

    def set_values(self, values: List[List[int]]):
        self.values = values

    def set_value(self, row: int, column: int, value: int) -> None:
        self.values[row][column] = value

    def toggle_selection(self, row: int, column: int) -> bool:
        new_val = not self.selection[row][column]
        self.selection[row][column] = new_val

        if self.selection[row][column]:
            self.row_selection[row] += 1
            self.col_selection[column] += 1
            self.dia_selection[0] += 1 if row == column else 0
            self.dia_selection[1] += 1 if row + column == self.size - 1 else 0

            if self.row_selection[row] >= self.size:
                self.row_bingo(row)

            if self.col_selection[column] == self.size:
                self.col_bingo(column)

            if row == column and self.dia_selection[0] >= self.size:
                self.dia_bingo(0)

            if row + column == self.size - 1 and self.dia_selection[1] >= self.size:
                self.dia_bingo(1)

            if (column == 0 or column == self.size - 1) and (row == 0 or row == self.size - 1) and \
                    self.selection[0][0] and \
                    self.selection[0][self.size - 1] and \
                    self.selection[self.size - 1][0] and \
                    self.selection[self.size - 1][self.size - 1]:
                self.banana_bingo()

            return True
        self.row_selection[row] -= 1
        self.col_selection[column] -= 1
        self.dia_selection[0] -= 1 if row == column else 0
        self.dia_selection[1] -= 1 if row + column == self.size - 1 else 0
        return False

    def row_bingo(self, row: int) -> int:
        rsum = sum(self.values[row])
        self.score += rsum * 10 * self.bingos
        self.bingos += 1
        show_bingo_row(row, self.board, self.size)
        return self.score

    def col_bingo(self, column: int) -> int:
        csum = 0
        for row in self.values:
            csum += row[column]
        self.score += csum * 10 * self.bingos
        self.bingos += 1
        show_bingo_column(column, self.board, self.size)
        return self.score

    def dia_bingo(self, index: int):
        dsum = 0
        if index == 0:
            for row in range(len(self.values)):
                dsum += self.values[row][row]
        elif index == 1:
            for row in range(len(self.values)):
                dsum += self.values[row][self.size - row - 1]
        self.score += dsum * 10 * self.bingos
        self.bingos += 1
        show_bingo_diagonal(index, self.board, self.size)
        return self.score

    def banana_bingo(self):
        bsum = self.values[0][0]
        bsum += self.values[0][self.size - 1]
        bsum += self.values[self.size - 1][0]
        bsum += self.values[self.size - 1][self.size - 1]
        self.score += bsum * 3 * self.bingos
        self.bingos += 1
        show_banana_bingo(self.board, self.size)
        return self.score
