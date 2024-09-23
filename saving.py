import datetime
import os


def load_or_create_profile_file(path: str = "."):
    profile_lines = []
    try:
        with open(path + '/profile.txt', 'rt', encoding="utf-8") as profile_file:
            profile_lines = profile_file.readlines()
    except FileNotFoundError:
        with open(path + '/profile.txt', 'xt', encoding="utf-8") as profile_file:
            profile_lines = [
                f"last_updated={datetime.datetime.now().isoformat()} \n",
                'score=0\n',
                'games_played=0\n',
                'saved_games=[]\n',
                'game_path=.\n',
                f'profile_path={path}/profile.txt\n'
            ]
            profile_file.writelines(profile_lines)
    profile = {}
    try:
        for line in profile_lines:
            name, value = line[:-1].split("=")
            profile[name] = value
    except ValueError:
        print("could not read profile, creating new")
        os.makedirs(path + '/loading_error_profiles', exist_ok=True)

        profile = load_or_create_profile_file(path=path + '/loading_error_profiles')
    return profile


def update_profile(profile: dict) -> None:
    """
    Overrides the profile file by the new content in the profile-dict
    :param profile: a dict containing all the options as keys and the values as vals
    """
    with open(profile['profile_path'], 'wt', encoding="utf-8") as profile_file:
        lines = [f"last_updated={datetime.datetime.now().isoformat()} \n"]
        for key, value in profile.items():
            if key == 'last_updated':
                continue
            lines += [f"{key}={value}\n"]
        profile_file.writelines(lines)


def save_game(path: str, number:int , game: dict) -> None:
    path += f"/game_{number}.txt"
    try:
        with open(path, "xt", encoding="utf-8") as game_file:
            pass
    except FileExistsError:
        pass
    finally:
        with open(path, "wt", encoding="utf-8") as game_file:
            lines = [f"{key}={value}\n" for key, value in game.items()]
            game_file.writelines(lines)


def load_game_save(path:str):
    game = {}
    with open(path, "r", encoding="utf-8") as game_file:
        for line in game_file.readlines():
            key, value = line[:-1].split("=")
            game[key] = value

    return game

