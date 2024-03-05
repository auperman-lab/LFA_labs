import os.path
import random
from grammar import Grammar
from lab2.finiteAutomaton import FiniteAutomaton


class Main:

    @staticmethod
    def generate_valid_strings(grammar, num_strings):
        valid_strings = []

        def generate_string(remaining_string, transition):
            if not remaining_string:
                return '', transition

            for index, char in enumerate(remaining_string):
                if char.isupper():
                    current_symbol = char
                    break
            else:
                return remaining_string, transition

            if current_symbol in grammar.VT:
                current_string, transition = generate_string(remaining_string[index + 1:], transition)
                return current_symbol + current_string, transition
            else:
                production = random.choice(grammar.P[current_symbol])
                new_remaining_string = ''.join(reversed(production)) + remaining_string[index + 1:]
                transition.append((current_symbol, production))
                return generate_string(new_remaining_string, transition)

        for _ in range(num_strings):
            string, transitions = generate_string('S', [('S', 'S')])
            valid_strings.append((string[::-1], transitions))

        return valid_strings

    @staticmethod
    def run():

        grammar = Grammar()

        print("Generated strings:")
        valid_strings = Main.generate_valid_strings(grammar, 5)

        for result, transitions in valid_strings:
            for transition in transitions:
                print(f"-> {transition[1]}", end=' ')
            print(f"-> {result} \n")

        finite_automaton = FiniteAutomaton(grammar)

        chomsky_type = grammar.chomsky_classification()
        print("\n\nChomsky Classification:", chomsky_type)

        regular_grammar = finite_automaton.convert_to_regular_grammar()
        print("\n\nFA to grammar")
        regular_grammar.print_grammar()

        faType = finite_automaton.check_dfa_or_nfa()
        print("\n\nDFA or NFA : ", faType)

        dfa = finite_automaton.convert_ndfa_to_dfa()
        print("NFA after conversion :")
        print(dfa)

        dfaType = finite_automaton.check_dfa_or_nfa()
        print("\n\nDFA or NFA : ", dfaType)


if os.path.basename(__file__) == "main.py":
    Main.run()
