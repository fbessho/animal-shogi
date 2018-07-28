from .board import INITIAL_BOARD
from .node import Node


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
