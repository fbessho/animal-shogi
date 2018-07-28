from copy import copy
import json
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


class Board(object):
    """
    +---+---+---+
    |1,1|1,2|1,3|
    +---+---+---+
    |2,1|2,2|2,3|
    +---+---+---+
    |3,1|3,2|3,3|
    +---+---+---+
    |4,1|4,2|4,3|
    +---+---+---+
    """
    SIZE_ROW = 4
    SIZE_COL = 3

    def __init__(self):
        self.my_mochigoma = {}    # type: Dict[Koma, int]
        self.your_mochigoma = {}  # type: Dict[Koma, int]
        self.my_board = {}        # type: Dict[Tuple[int, int], Koma]
        self.your_board = {}      # type: Dict[Tuple[int, int], Koma]
        self.my_turn = True

    def show(self):
        """Print the current board"""
        print self

    def to_dict(self):
        """
        Example returned dict:

        {
            'your_mochigoma': [],
            'my_mochigoma': [{'koma': 'FU', 'num': 1}],
            'board': [{'koma': 'OU', 'y': 2, 'mine': True, 'x': 1},
                      {'koma': 'HI', 'y': 3, 'mine': True, 'x': 1},
                      {'koma': 'KA', 'y': 1, 'mine': True, 'x': 1},
                      {'koma': 'FU', 'y': 2, 'mine': True, 'x': 2},
                      {'koma': 'OU', 'y': 2, 'mine': False, 'x': 4},
                      {'koma': 'HI', 'y': 1, 'mine': False, 'x': 4},
                      {'koma': 'KA', 'y': 3, 'mine': False, 'x': 4}]
        }
        """
        board = []
        for _board, mine in [(self.my_board, True), (self.your_board, False)]:
            for xy, koma in _board.items():
                x, y = xy
                board.append(dict(x=x, y=y, koma=koma.yomi, mine=mine))

        return {
            'my_mochigoma': [{"koma": k.yomi, "num": v} for k, v in self.my_mochigoma.items()],
            'your_mochigoma': [{"koma": k.yomi, "num": v} for k, v in self.your_mochigoma.items()],
            'board': board
        }

    def to_json(self, path_or_fp=None):
        # Return dict
        if path_or_fp is None:
            return json.dumps(self.to_dict())
        # Write to a file
        elif isinstance(path_or_fp, basestring):
            with open(path_or_fp, 'w') as fp:
                json.dump(self.to_dict(), fp)
        # Write to a buffer
        else:
            json.dump(self.to_dict(), path_or_fp)

    def __eq__(self, other):
        return equals(self, other)


    @staticmethod
    def _parse_row(row):
        r_value = []
        for i in range(Board.SIZE_COL):
            if row.startswith('*'):
                r_value.append(None)
            

    @classmethod
    def from_str(cls, s):
        b = Board()
        current_x = 0
        for row in s:
            s = s.replace(' ', '')
            if 'my_turn' in s:
                b.my_turn = True if 'true' in s.lower() else False
            elif s.startswith('*') or s.startswith('-') or s.startswith('+'):
                current_row += 1



    def __str__(self):
        s = []
        s.append('my_turn={}'.format(self.my_turn))
        s.append(','.join([k.yomi for k in self.your_mochigoma]))
        s.append('')
        for y in range(1, self.SIZE_ROW + 1):
            row = []
            for x in range(1, self.SIZE_COL + 1):
                if (x, y) in self.my_board:
                    row.append('+{}'.format(self.my_board[(x, y)].yomi))
                elif (x, y) in self.your_board:
                    row.append('-{}'.format(self.your_board[(x, y)].yomi))
                else:
                    row.append(' * ')
            s.append(''.join(row))
        s.append('')
        s.append(','.join([k.yomi for k in self.my_mochigoma]))
        return '\n'.join(s)

    def copy(self):
        """Return a copy of the current board"""
        b = Board()
        b.my_mochigoma = copy(self.my_mochigoma)
        b.your_mochigoma = copy(self.your_mochigoma)
        b.my_board = copy(self.my_board)
        b.your_board = copy(self.your_board)
        b.my_turn = self.my_turn
        return b

    def flip(self):
        """Return the same board but flipped internally"""
        b = Board()
        b.my_turn = not self.my_turn
        b.my_mochigoma = copy(self.your_mochigoma)
        b.your_mochigoma = copy(self.my_mochigoma)
        flip_xy = lambda (x, y): (self.SIZE_COL - x + 1, self.SIZE_ROW - y + 1)
        b.my_board = {flip_xy(coord): koma for coord, koma in self.your_board.iteritems()}
        b.your_board = {flip_xy(coord): koma for coord, koma in self.my_board.iteritems()}
        return b

    @property
    def score(self):
        _score = 0
        _score += sum([koma.score for koma in self.my_mochigoma])
        _score += sum([koma.score for koma in self.my_board.values()])
        _score -= sum([koma.score for koma in self.your_mochigoma])
        _score -= sum([koma.score for koma in self.your_board.values()])
        return _score

    @property
    def possible_nexts(self):
        """Returns Iterable[Board]"""
        # make sure current_oard.my_turn is True
        current_board = self if self.my_turn else self.flip()

        # 1. use mochigoma
        for koma in current_board.my_mochigoma:
            for r in range(1, self.SIZE_ROW+1):
                for c in range(1, self.SIZE_COL+1):
                    if current_board._blank(r, c):
                        board = current_board.copy()
                        board.my_turn = not board.my_turn
                        board.my_board[(r, c)] = koma
                        if board.my_mochigoma[koma] == 1:
                            board.my_mochigoma.pop(koma)
                        else:
                            # two or more mochigoma
                            board.my_mochigoma[koma] -= 1

                        # flip back before returning
                        if not self.my_turn:
                            board = board.flip()
                        yield board

        # 2. move my koma in the board
        for position, koma in current_board.my_board.items():
            for direction in koma.directions:
                # new position
                r, c = map(sum, zip(position, direction))
                if ((r, c) not in current_board.my_board) and self._valid(r, c):
                    board = current_board.copy()
                    # Take opponent's koma
                    if (r, c) in board.your_board:
                        koma = board.your_board.pop((r, c))
                        board.my_mochigoma[koma] = board.my_mochigoma.get(koma, 0) + 1
                    koma = board.my_board.pop(position)
                    board.my_board[(r, c)] = koma
                    board.my_turn = not board.my_turn
                    if not self.my_turn:
                        board = board.flip()
                    yield board

    def _blank(self, r, c):
        """Returns True if (r,c) is blank"""
        if (r, c) in self.my_board:
            return False
        if (r, c) in self.your_board:
            return False
        return True

    def _valid(self, r, c):
        """Returns True if (r, c) is a valid position"""
        return (1 <= r <= self.SIZE_ROW) and (1 <= c <= self.SIZE_COL)


class Node(object):
    def __init__(self, board, depth=3):
        self.board = board
        self.depth = depth
        self._score = None
        self.best_moves = None
        # self.last_move  # TODO: implement

    @property
    def score(self):
        if self._score is None:
            raise RuntimeError("Run evaluate() first")
        return self._score

    @property
    def child_nodes(self):
        if self.depth == 0:
            return []
        return [Node(board, depth=self.depth - 1) for board in self.board.possible_nexts]

    def evaluate(self):
        """
        - Calculate score
        - Store the best moves
        """
        # Return the score of the board if this doesn't need to check further
        if self.depth == 0:
            self._score = self.board.score
            self.best_moves = [self.board]
            return

        # Else check child nodes and take the max if it's my turn, else the min
        if self.board.my_turn:
            minmax = max
            best_score = -1 * 10 ** 200
            best_node = None
        else:
            minmax = min
            best_score = 10**200
            best_node = None
        for n in self.child_nodes:
            n.evaluate()
            s = minmax(best_score, n.score)
            if s != best_score:
                # updating..
                best_node = n
                best_score = s
        self._score = best_score
        self.best_moves = [self.board] + best_node.best_moves

    @property
    def possible_nexts(self):
        """

        :return: iterator of Node
        """
        for board in self.board.possible_nexts:
            yield Node(board, self.depth-1)


class Koma(object):
    def __init__(self, directions, score, yomi):
        self.directions = directions
        self.score = score
        self.yomi = yomi

    def __repr__(self):
        return '<Koma {}>'.format(self.yomi)


LION = Koma([[-1, 1], [-1, 0], [-1, -1], [0, 1], [0, -1], [1, 1], [1, 0], [1, -1]], 100, 'OU')
GIRAFFE = Koma([[-1, 0], [0, 1], [0, -1], [1, 0]], 4, 'HI')
ELEPHANT = Koma([[-1, 1], [-1, -1], [1, 1], [1, -1]], 4, 'KA')
CHICKEN = Koma([[0, -1], [1, -1], [1, 0], [0, 1], [-1, 0], [-1, -1]], 4, 'TO')
CHICK = Koma([[0, -1]], 3, 'FU')

INITIAL_BOARD = Board()
INITIAL_BOARD.my_board = {(1, 4): ELEPHANT, (2, 4): LION, (3, 4): GIRAFFE, (2, 3): CHICK}
INITIAL_BOARD.your_board = {(3, 1): ELEPHANT, (2, 1): LION, (1, 1): GIRAFFE, (2, 2): CHICK}


def main():
    b = INITIAL_BOARD
    while True:
        b.show()
        n = Node(b, depth=6)
        n.evaluate()
        print 'Score: {}'.format(n.score)
        print 'Best moves:'
        for b in n.best_moves:
            print b
            print
        break


if __name__ == '__main__':
    main()
