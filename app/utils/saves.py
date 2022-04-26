from datetime import datetime


def create_puz_id_list(save_id: int, puz_id_list: str) -> list:
    puz_list = list(map(lambda row: (int(row), datetime.now(), save_id), puz_id_list.split(';')))
    return puz_list
