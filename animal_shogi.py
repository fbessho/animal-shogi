"""


Japanese-English
Koma -> A piece
Niwatori -> Chicken
Hiyoko -> Chick
"""

class Board(object):
    def __init__(self):
        self.my_mochigoma = []
        self.your_mochigoma = []
        self.my_board = {}
        self.your_board = {}

    def show(self):
        """Print the current board"""
        print ','.join([k.yomi for k in self.your_mochigoma])
        print ''
        for i in range(4, 0, -1):
            row = []
            for j in range(1, 4):
                if (i, j) in self.my_board:
                    row.append('+{}'.format(self.my_board[(i, j)].yomi))
                elif (i, j) in self.your_board:
                    row.append('-{}'.format(self.your_board[(i, j)].yomi))
                else:
                    row.append(' * ')
            print ''.join(row)
        print ''
        print ','.join([k.yomi for k in self.my_mochigoma])

    @property
    def score(self):
        # TODO: implement
        pass


class Node(object):
    def __init__(self, board, my_turn, depth=3):
        self.board = board
        self.my_turn = my_turn
        self.depth = depth
        self._score = None

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




class Koma(object):
    def __init__(self, directions, score, yomi):
        self.score = score
        self.directions = directions
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
