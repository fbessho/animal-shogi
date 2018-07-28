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
