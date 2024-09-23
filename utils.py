from ast import literal_eval


def str_to_list(string: str) -> list:
    return literal_eval(string)


