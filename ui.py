import tkinter as tk
from typing import List


def show_bingo(board: List[List[str]], scoring) -> None:
    bingo_window_root = tk.Tk(screenName="Bahnbingo")
    bingo_window_root.title("Bahnbingo")
    bingo_window_root.resizable(width=False, height=False)
    bingo_window = tk.Frame(bingo_window_root)

    bingo_window.grid()
    buttons = []
    for rindex, row in enumerate(board):
        for cindex, col in enumerate(board[rindex]):
            button = tk.Button(bingo_window,
                               text=col,
                               command=lambda index=len(buttons), r=rindex, c=cindex: \
                                   on_bingo_button_click(buttons[index], r, c, scoring),
                               width=16,
                               height=7,
                               bg="#f0f0f0",
                               borderwidth=0
                               )
            button.grid(row=rindex, column=cindex, padx=2, pady=2)
            buttons += [button]
    spacer = tk.Label()
    spacer.grid(row=len(board))
    scoring.set_board(buttons)
    bingo_window.mainloop()



def on_bingo_button_click(button: tk.Button, row: int, col: int, scoring) -> None:
    if button.cget('bg') == "#f0f0f0":
        button.config(bg="lightgray")
    else:
        button.config(bg="#f0f0f0")
    scoring.toggle_selection(row, col)


def show_bingo_row(row: int, board: List[tk.Button], size: int) -> None:
    index = size * row
    while index < size * (row + 1):
        board[index].config(bg="#bfa100", state="disabled")
        index += 1


def show_bingo_column(column: int, board: List[tk.Button], size: int):
    index = column
    while index < len(board):
        board[index].config(bg="#bfa100", state="disabled")
        index += size


def show_bingo_diagonal(diagonal: int, board: List[tk.Button], size: int):
    if diagonal == 0:
        for offset in range(size):
            board[size * offset + offset].config(bg="#bfa100", state="disabled")

    elif diagonal == 1:
        for offset in range(size):
            board[size * offset + (size - offset-1)].config(bg="#bfa100", state="disabled")


def show_banana_bingo(board: List[tk.Button], size: int) -> None:
    board[0].config(bg="#fdcb43", state="disabled")
    board[size - 1].config(bg="#fdcb43", state="disabled")
    board[size ** 2 - 1].config(bg="#fdcb43", state="disabled")
    board[size ** 2 - size ].config(bg="#fdcb43", state="disabled")


if __name__ == "__main__":
    show_bingo(
        [["1", "2", "3", "4", "5"], ["1", "2", "3", "4", "5"], ["1", "2", "3", "4", "5"], ["1", "2", "3", "4", "5"],
         ["1", "2", "3", "4", "5"]])
