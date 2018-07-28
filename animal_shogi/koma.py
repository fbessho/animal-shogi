class Koma(object):
    def __init__(self, directions, score, yomi):
        self.directions = directions
        self.score = score
        self.yomi = yomi

    def __repr__(self):
        return '<Koma {}>'.format(self.yomi)

    @classmethod
    def from_str(cls, yomi):
        return ALL_KOMA[yomi]


LION = Koma([[-1, 1], [-1, 0], [-1, -1], [0, 1], [0, -1], [1, 1], [1, 0], [1, -1]], 100, 'OU')
GIRAFFE = Koma([[-1, 0], [0, 1], [0, -1], [1, 0]], 4, 'HI')
ELEPHANT = Koma([[-1, 1], [-1, -1], [1, 1], [1, -1]], 4, 'KA')
CHICKEN = Koma([[0, -1], [1, -1], [1, 0], [0, 1], [-1, 0], [-1, -1]], 4, 'TO')
CHICK = Koma([[0, -1]], 3, 'FU')

ALL_KOMA = {
    'OU': LION, 'HI': GIRAFFE, 'KA': ELEPHANT, 'TO': CHICKEN, 'FU': CHICK
}
