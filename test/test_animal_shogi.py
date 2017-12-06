from animal_shogi import INITIAL_BOARD

from textwrap import dedent


class TestBoard():
    def test_flip(self):
        expected = """\
        
        
        -HI-OU-KA
         * -FU * 
         * +FU * 
        +KA+OU+HI
        
        """

        actual = str(INITIAL_BOARD.flip())
        assert dedent(expected) == actual
