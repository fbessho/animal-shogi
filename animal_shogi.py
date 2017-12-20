"""


Japanese-English
Koma -> A piece
Niwatori -> Chicken
Hiyoko -> Chick
"""
from copy import copy
import re


def simplify(board):
    b = str(board)
    b = b.replace(' ', '')
    b = re.sub(r'^$', '', b, flags=re.MULTILINE)
    b = b.strip()
    return b


def equals(board1, board2):
    board1 = str(board1)
    board2 = str(board2)
    return simplify(board1) == simplify(board2)


class Board(object):
    """


    your_mochigoma: (5,0)
    +---+---+---+
    |4,1|4,2|4,3|
    +---+---+---+
    |3,1|3,2|3,3|
    +---+---+---+
    |2,1|2,2|2,3|
    +---+---+---+
    |1,1|1,2|1,3|
    +---+---+---+
    my_mochigoma: (0, 0)

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

    def __eq__(self, other):
        return equals(self, other)

    def __str__(self):
        s = []
        s.append(','.join([k.yomi for k in self.your_mochigoma]))
        s.append('')
        for i in range(self.SIZE_ROW, 0, -1):
            row = []
            for j in range(1, self.SIZE_COL + 1):
                if (i, j) in self.my_board:
                    row.append('+{}'.format(self.my_board[(i, j)].yomi))
                elif (i, j) in self.your_board:
                    row.append('-{}'.format(self.your_board[(i, j)].yomi))
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
        flip_xy = lambda (x, y): (self.SIZE_ROW - x + 1, self.SIZE_COL - y + 1)
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
        # TODO: support when self.my_turn is False

        # 1. use mochigoma
        for koma in self.my_mochigoma:
            for r in range(1, self.SIZE_ROW+1):
                for c in range(1, self.SIZE_COL+1):
                    if self._blank(r, c):
                        board = self.copy()
                        board.my_turn = not board.my_turn
                        board.my_board[(r, c)] = koma
                        if board.my_mochigoma[koma] == 1:
                            board.my_mochigoma.pop(koma)
                        else:
                            # two or more mochigoma
                            board.my_mochigoma[koma] -= 1
                        yield board

        # 2. move my koma in the board
        for position, koma in self.my_board.items():
            for direction in koma.directions:
                # new position
                r, c = map(sum, zip(position, direction))
                if ((r, c) not in self.my_board) and self._valid(r, c):
                    board = self.copy()
                    # Take opponent's koma
                    if (r, c) in board.your_board:
                        koma = board.your_board.pop((r, c))
                        board.my_mochigoma[koma] = board.my_mochigoma.get(koma, 0) + 1
                    koma = board.my_board.pop(position)
                    board.my_board[(r, c)] = koma
                    board.my_turn = not board.my_turn
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
    def __init__(self, board, my_turn=True, depth=3):
        self.board = board
        self.my_turn = my_turn
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
        return [Node(board, not self.my_turn, depth=self.depth - 1) for board in self.board.possible_nexts]

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
        if self.my_turn:
            minmax = max
            best_score = -100
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
            yield Node(board, not self.my_turn, self.depth-1)


class Koma(object):
    def __init__(self, directions, score, yomi):
        self.directions = directions
        self.score = score
        self.yomi = yomi


LION = Koma([[-1, 1], [-1, 0], [-1, -1], [0, 1], [0, -1], [1, 1], [1, 0], [1, -1]], 100, 'OU')
GIRAFFE = Koma([[-1, 0], [0, 1], [0, -1], [1, 0]], 4, 'HI')
ELEPHANT = Koma([[-1, 1], [-1, -1], [1, 1], [1, -1]], 4, 'KA')
CHICKEN = Koma([[-1, 1], [-1, 0], [0, 1], [0, -1], [1, 1], [1, 0]], 4, 'TO')
CHICK = Koma([[1, 0]], 3, 'FU')

INITIAL_BOARD = Board()
INITIAL_BOARD.my_board = {(1, 1): ELEPHANT, (1, 2): LION, (1, 3): GIRAFFE, (2, 2): CHICK}
INITIAL_BOARD.your_board = {(4, 3): ELEPHANT, (4, 2): LION, (4, 1): GIRAFFE, (3, 2): CHICK}


def main():
    b = INITIAL_BOARD
    while True:
        b.show()
        n = Node(b, depth=5)
        n.evaluate()
        print 'Score: {}'.format(n.score)
        print 'Best moves:'
        for b in n.best_moves:
            print b
            print
        break


if __name__ == '__main__':
    main()
