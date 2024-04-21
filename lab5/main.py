import os

from lab5.chomskyConverter import ChomskyConverter
from lab5.grammar import Grammar


class Main:

    @staticmethod
    def run():
        my_grammar = Grammar(VN={'S', 'A', 'B', 'C', 'D', 'X'},
                             VT={'a', 'b'},
                             P={
                                 'S': {'A'},
                                 'A': {'aX', 'bX'},
                                 'X': {'', 'BX', 'b'},
                                 'B': {'AD'},
                                 'D': {'aD', 'a'},
                                 'C': {'Ca'}
                             })
        print(my_grammar)

        convertor = ChomskyConverter(my_grammar.VN, my_grammar.VT, my_grammar.P)
        upd_grammar = convertor.convert()

        print(upd_grammar)


if os.path.basename(__file__) == "main.py":
    Main.run()
