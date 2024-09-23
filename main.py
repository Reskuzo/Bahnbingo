from create_board import create_board
import saving
import scoring
from bingo_ui import show_bingo
from utils import str_to_list


def load_default_game_settings() -> dict:
    return {'size': 5, 'difficulty': 25, 'ice': False, 'Score': 0, 'board': [], 'name': 'Bahnbingo', 'profile_path': '.'}


def start_game(profile: dict, game: dict) -> None:
    score_observer = scoring.Score(int(game['size']))
    profile['games_played'] = int(profile['games_played']) + 1
    create_board(game=game, score_observer=score_observer, profile=profile)
    show_bingo(game=game, score_observer=score_observer)


if __name__ == '__main__':
    # start new game
    profile = saving.load_or_create_profile_file()
    games_saved = str_to_list(profile['saved_games'])
    if len(games_saved) > 0:
        game = saving.load_game_save(games_saved[-1])
    else:
        game = load_default_game_settings()
    start_game(profile=profile, game=game)





