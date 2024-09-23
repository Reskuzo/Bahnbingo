import random
from typing import List, Tuple

import saving
from scoring import Score
from utils import str_to_list


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


def create_board(game: dict, score_observer: Score, profile: dict) -> None:
    full_board = []
    success = False
    difficulty = game['difficulty']
    size = game['size']
    ice = game['ice']
    if len(str_to_list(game['board'])) != 0:
        game['board'] = str_to_list(game['board'])
        return
    while not success:
        full_board = []
        tasks = read_bingo_tasks(r"./tasks.txt", ice)
        success = True
        row_difficulty = [difficulty]*size
        col_difficulty = [difficulty]*size
        dia_difficulty = [difficulty]*2

        chosen_lines = []

        for row in range(size):
            for col in range(size):
                max_difficulty = min(row_difficulty[row],
                                     col_difficulty[col],
                                     dia_difficulty[0] if row == col else difficulty,
                                     dia_difficulty[1] if row + col == size else difficulty)
                valid_tasks = []
                for task in tasks:
                    if task[0] <= max_difficulty:
                        valid_tasks += [task] * task[0]

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

                full_board += [(chosen_difficulty, chosen_line)]

                chosen_lines += [chosen_line]

                for index, task in enumerate(tasks):
                    if chosen_line in task[1]:
                        tasks[index][1].remove(chosen_line)
                        if len(tasks[index][1]) == 0:
                            tasks.remove(tasks[index])
                        break

                score_observer.set_value(row, col, chosen_difficulty)

            else:
                continue
            break
    game['board'] = full_board
    profile['saved_games'] = str_to_list(profile['saved_games']) + [f"{profile['game_path']}/game_{profile['games_played']}.txt"]
    saving.save_game(game=game, number=profile['games_played'], path=profile['game_path'])
    saving.update_profile(profile)
