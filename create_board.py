import random
from typing import List, Tuple

from scoring import Score


def read_bingo_tasks(filepath: str, ice: bool) -> List[Tuple[int, List[str]]]:
    result = []
    with open(filepath, 'r', encoding='utf-8') as bingo_file:
        for line in bingo_file.readlines():
            line_split = line.split(";")

            # if you're playing regio filter out ice
            if not ice and line_split[0] == "1":
                continue

            difficulty = int(line_split[1])
            content = line_split[2][:-1]
            content = content.replace("\\", "\n")
            inserted = False
            for diff, lines in result:
                if difficulty == diff:
                    lines.append(content)
                    inserted = True
            if not inserted:
                result.append((difficulty, [content]))
    return result


def create_board(difficulty: int, size: int, ice: bool, scoring: Score) -> List[List[str]]:
    success = False
    while not success:
        board = []
        tasks = read_bingo_tasks(r"./tasks.txt", ice)
        success = True
        row_difficulty = [difficulty]*size
        col_difficulty = [difficulty]*size
        dia_difficulty = [difficulty]*2

        for row in range(size):
            board += [[]]
            for col in range(size):
                max_difficulty = min(row_difficulty[row],
                                     col_difficulty[col],
                                     dia_difficulty[0] if row == col else difficulty,
                                     dia_difficulty[1] if row + col == size else difficulty)
                valid_tasks = []
                for task in tasks:
                    if task[0] <= max_difficulty:
                        valid_tasks += [task]

                if len(valid_tasks) == 0:
                    success = False
                    print("Failed to build board")
                    break

                dif_ind = random.randint(0, len(valid_tasks) - 1)
                chosen_difficulty, valid_lines = valid_tasks[dif_ind]
                row_difficulty[row] -= chosen_difficulty
                col_difficulty[col] -= chosen_difficulty
                dia_difficulty[1] -= chosen_difficulty if row + col == size else 0
                dia_difficulty[0] -= chosen_difficulty if row == col else 0

                chosen_line = valid_lines[random.randint(0, len(valid_lines)-1)]

                if chosen_line in tasks[dif_ind][1]:
                    tasks[dif_ind][1].remove(chosen_line)
                    if len(tasks[dif_ind][1]) == 0:
                        tasks.remove(tasks[dif_ind])

                board[row] += [chosen_line]

                scoring.set_value(row, col, chosen_difficulty)

            else:
                continue
            break
    return board


if __name__ == "__main__":
    import ui
    ui.show_bingo(create_board(20, 5, True, Score(5)),Score(5))
