"""


Japanese-English
Koma -> A piece
Niwatori -> Chicken
Hiyoko -> Chick
"""


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
        self.my_mochigoma = []
        self.your_mochigoma = []
        self.my_board = {}
        self.your_board = {}
        self.my_turn = True

    def show(self):
        """Print the current board"""
        print self

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

    def flip(self):
        """Return the same board but flipped internally"""
        b = Board()
        b.my_turn = not self.my_turn
        b.my_mochigoma = self.your_mochigoma[:]
        b.your_mochigoma = self.my_mochigoma[:]
        flip_xy = lambda (x, y): (self.SIZE_ROW - x + 1, self.SIZE_COL - y + 1)
        b.my_board = {flip_xy(coord): koma for coord, koma in self.your_board.iteritems()}
        b.your_board = {flip_xy(coord): koma for coord, koma in self.my_board.iteritems()}
        return b

    @property
    def score(self):
        _score = 0
        _score += [koma.score for koma in self.my_mochigoma]
        _score += [koma.score for koma in self.my_board.values()]
        _score -= [koma.score for koma in self.your_mochigoma]
        _score -= [koma.score for koma in self.your_board.values()]
        return _score

    @property
    def possible_nexts(self):
        pass  # TODO: implement

        # 1. move my koma on the board
        # 2. use mochigoma


class Node(object):
    def __init__(self, board, my_turn, depth=3):
        self.board = board
        self.my_turn = my_turn
        self.depth = depth
        self._score = None
        self.best_moves  # TODO: implement
        self.last_move  # TODO: implement

    @property
    def score(self):
        if self._score is None:
            raise RuntimeError("Run evaluate() first")
        return self._score

    @property
    def child_nodes(self):
        if self.depth == 0:
            return None  # TODO: should return an empty array?
        return [Node(board, not self.my_turn, depth=self.depth - 1) for board in self.board.possible_nexts]

    def evaluate(self):
        """Calculate score"""
        # Return the score of the board if this doesn't need to check further
        if self.depth == 0:
            return self.board.score

        # Else check child nodes and take the max if it's my turn, else the min
        if self.my_turn:
            self._score = max([n.score for n in self.child_nodes])
        else:
            self._score = max([n.score for n in self.child_nodes])

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
CHICK = Koma([[0, 1]], 3, 'FU')

INITIAL_BOARD = Board()
INITIAL_BOARD.my_board = {(1, 1): ELEPHANT, (1, 2): LION, (1, 3): GIRAFFE, (2, 2): CHICK}
INITIAL_BOARD.your_board = {(4, 3): ELEPHANT, (4, 2): LION, (4, 1): GIRAFFE, (3, 2): CHICK}


def main():
    b = INITIAL_BOARD
    while True:
        b.show()
        n = Node(b, depth=3)
        n.evaluate()
        print 'Score: {}'.format(n.score)
        print 'Best moves: \n{}'.format(n.best_moves)
        move = raw_input('Input move: ')


if __name__ == '__main__':
    main()
