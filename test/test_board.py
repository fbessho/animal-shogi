from animal_shogi.board import Board, INITIAL_BOARD
from animal_shogi.utils import equals, simplify, normalize_board_dict


def assert_board_equal(expected, actual):
    if not equals(expected, actual):
        print "== Expected =="
        print expected
        print "\n== Actual =="
        print actual
        raise AssertionError("Boards are not equal")


class TestBoard:
    def test_to_dict(self):
        board = INITIAL_BOARD.copy()
        koma = board.your_board.pop((2, 2))
        board.my_mochigoma[koma] = 1

        expected = {
            'your_mochigoma': [],
            'my_mochigoma': [
                {'koma': 'FU', 'num': 1}
            ],
            'board': [
                {'koma': 'OU', 'mine': True, 'x': 2, 'y': 4},
                {'koma': 'HI', 'mine': True, 'x': 3, 'y': 4},
                {'koma': 'KA', 'mine': True, 'x': 1, 'y': 4},
                {'koma': 'FU', 'mine': True, 'x': 2, 'y': 3},
                {'koma': 'OU', 'mine': False, 'x': 2, 'y': 1},
                {'koma': 'HI', 'mine': False, 'x': 1, 'y': 1},
                {'koma': 'KA', 'mine': False, 'x': 3, 'y': 1}
            ]
        }
        assert normalize_board_dict(expected) == board.to_dict()

    def test_from_str(self):
        board_str = """        
        my_turn=True
        
        
         * -OU-KA
         *  *  * 
         *  *  * 
        +KA+OU *
        
        HI2 FU2
        """
        board = Board.from_str(board_str)
        assert_board_equal(board_str, str(board))

    def test_to_str(self):
        expected = """
        my_turn=True
        -HI-OU-KA
         * -FU *
         * +FU *
        +KA+OU+HI
        """
        assert_board_equal(expected, str(INITIAL_BOARD))

    def test_flip(self):
        expected = """
        my_turn=False
        -HI-OU-KA
         * -FU * 
         * +FU * 
        +KA+OU+HI
        """

        actual = str(INITIAL_BOARD.flip())
        assert_board_equal(expected, actual)

    def test_possible_moves_from_initial_position(self):
        actual = set(INITIAL_BOARD.possible_nexts)
        actual = {simplify(board) for board in actual}
        expected = {
            """
            my_turn=False
            -HI-OU-KA
             * -FU * 
             * +FU+OU
            +KA * +HI
            """,

            """
            my_turn=False
            -HI-OU-KA
             * -FU * 
            +OU+FU * 
            +KA * +HI
            """,

            """
            my_turn=False
            -HI-OU-KA
             * -FU * 
             * +FU+HI
            +KA+OU * 
            """,

            """
            my_turn=False
            -HI-OU-KA
             * +FU * 
             *  *  * 
            +KA+OU+HI
            
            FU
            """
        }
        expected = {simplify(board) for board in expected}
        assert expected == actual

    def test_possible_moves_with_mochigoma(self):
        board = INITIAL_BOARD.copy()
        koma = board.your_board.pop((2, 2))
        board.my_mochigoma[koma] = 1

        actual = board.possible_nexts
        actual = {simplify(board) for board in actual}
        expected = """
            my_turn=False
            -HI-OU-KA
             *  *  * 
            +FU+FU * 
            +KA+OU+HI
            
            
            my_turn=False            
            -HI-OU-KA
             *  *  * 
             * +FU+FU
            +KA+OU+HI
            
            
            my_turn=False            
            -HI-OU-KA
            +FU *  * 
             * +FU * 
            +KA+OU+HI
            
            
            my_turn=False            
            -HI-OU-KA
             * +FU * 
             * +FU * 
            +KA+OU+HI
            
            
            my_turn=False            
            -HI-OU-KA
             *  * +FU
             * +FU * 
            +KA+OU+HI
            
            
            my_turn=False            
            -HI-OU-KA
             *  *  * 
             * +FU+OU
            +KA * +HI
            
            FU
            
            
            my_turn=False            
            -HI-OU-KA
             *  *  * 
            +OU+FU * 
            +KA * +HI
            
            FU
            
            
            my_turn=False            
            -HI-OU-KA
             *  *  * 
             * +FU+HI
            +KA+OU * 
            
            FU
            
            
            my_turn=False            
            -HI-OU-KA
             * +FU * 
             *  *  * 
            +KA+OU+HI
            
            FU
        """
        expected = expected.replace(' ', '').split('\n\n\n')
        expected = {simplify(board) for board in expected}
        assert expected == actual
