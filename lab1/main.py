import os.path
import random
from grammar import Grammar
from lab1.finiteAutomaton import FiniteAutomaton


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

        input_strings = ['baca', "aa", "dawada", "aaba", "babca"]
        print("\nChecking if input strings can be created with actual Grammar:")
        for input_string in input_strings:

            if finite_automaton.check_string(input_string):
                print(f"'{input_string}' can be created with actual Grammar")
            else:
                print(f"'{input_string}' can't be created with actual Grammar")


if os.path.basename(__file__) == "main.py":

    Main.run()
