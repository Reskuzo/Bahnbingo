import create_board
import scoring
import ui

if __name__ == '__main__':
    # settings
    board_size = 5
    difficulty = 15
    ice = False

    # logic
    scoring = scoring.Score(board_size)
    board = create_board.create_board(difficulty, board_size, ice, scoring)
    ui.show_bingo(board, scoring)


