from animal_shogi import INITIAL_BOARD, equals, simplify


class TestBoard:
    def test_to_dict(self):
        board = INITIAL_BOARD.copy()
        koma = board.your_board.pop((3, 2))
        board.my_mochigoma[koma] = 1

        expected = {
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
        assert expected == board.to_dict()

    def test_flip(self):
        expected = """
        my_turn=False
        -HI-OU-KA
         * -FU * 
         * +FU * 
        +KA+OU+HI
        """

        actual = str(INITIAL_BOARD.flip())
        assert equals(expected, actual)

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
        koma = board.your_board.pop((3, 2))
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
