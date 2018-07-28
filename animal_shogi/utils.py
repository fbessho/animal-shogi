import re


def simplify(board):
    b = str(board)
    b = b.replace(' ', '')
    b = re.sub(r'^$\n', '', b, flags=re.MULTILINE)
    b = b.strip()
    return b


def equals(board1, board2):
    board1 = str(board1)
    board2 = str(board2)
    return simplify(board1) == simplify(board2)


def sort_key_board(koma):
    return koma['x'], koma['y'], koma['mine'], koma['koma']


def sort_key_mochigoma(koma):
    return koma['koma'], koma['num']


def normalize_board_dict(b):
    return {
        'my_mochigoma': sorted(b['my_mochigoma'], key=sort_key_mochigoma),
        'your_mochigoma': sorted(b['your_mochigoma'], key=sort_key_mochigoma),
        'board': sorted(b['board'], key=sort_key_board)
    }
