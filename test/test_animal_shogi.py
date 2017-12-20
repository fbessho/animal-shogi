from animal_shogi import INITIAL_BOARD, equals, simplify


class TestBoard:
    def test_flip(self):
        expected = """
        -HI-OU-KA
         * -FU * 
         * +FU * 
        +KA+OU+HI
        """

        actual = str(INITIAL_BOARD.flip())
        assert equals(expected, actual)

    def test_possible_moves(self):
        actual = set(INITIAL_BOARD.possible_nexts)
        actual = {simplify(board) for board in actual}
        expected = {
            """
            -HI-OU-KA
             * -FU * 
             * +FU+OU
            +KA * +HI
            """,

            """
            -HI-OU-KA
             * -FU * 
            +OU+FU * 
            +KA * +HI
            """,

            """
            -HI-OU-KA
             * -FU * 
             * +FU+HI
            +KA+OU * 
            """,

            """
            -HI-OU-KA
             * +FU * 
             *  *  * 
            +KA+OU+HI
            
            FU
            """
        }
        expected = {simplify(board) for board in expected}
        assert expected == actual
