from lab2.grammar import Grammar


class FiniteAutomaton:
    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None, grammar=None):
        if grammar:
            self.states = {}
            self.alphabet = {}
            self.transitions = {}
            self.initial_state = None
            self.final_states = {}
            self.convert_from_grammar(grammar)
        else:
            self.states = states
            self.alphabet = alphabet
            self.transitions = transitions
            self.initial_state = initial_state
            self.final_states = final_states

    def convert_from_grammar(self, grammar):

        self.states = grammar.VN
        self.alphabet = grammar.VT

        for symbol in grammar.P:
            for production in grammar.P[symbol]:
                if len(production) == 1:
                    self.transitions[(symbol, production)] = ['final']
                else:
                    self.transitions.setdefault((symbol, production[0]), []).append(production[1])

        self.initial_state = 'S'
        self.final_states = {symbol for symbol in grammar.P if symbol.isupper()}

    def check_string(self, input_string):

        current_state = self.initial_state

        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False

        return True

    def convert_to_regular_grammar(self):
        regular_grammar = Grammar()

        # Set the states and alphabet
        regular_grammar.VN = self.states
        regular_grammar.VT = self.alphabet

        # Reset the productions
        regular_grammar.P = {}

        for (source, target), destination in self.transitions.items():
            if destination[0] == 'final':
                regular_grammar.P.setdefault(source, []).append(target)
            else:
                for item in destination:
                    regular_grammar.P.setdefault(source, []).append(target + item)

        return regular_grammar

    def check_dfa_or_nfa(self):
        is_dfa = True

        for qwer, trans in self.transitions.items():
            if len(trans) > 1:
                is_dfa = False
                break

        return "DFA" if is_dfa else "NFA"

    def convert_ndfa_to_dfa(self):
        init_state = self.initial_state
        dfa_table = {(frozenset(init_state), alpha): [] for alpha in self.alphabet}
        states = set(init_state)
        x = 1
        while x != 0:
            x = 0
            keys_to_process = [key for key, value in dfa_table.items() if value == []]

            for dfa_states in keys_to_process:
                symbol = dfa_states[1]
                for state in dfa_states[0]:
                    dfa_table[dfa_states] = dfa_table.get(dfa_states, []) + self.transitions.get((state, symbol), [])

                for alpha in self.alphabet:
                    if dfa_table[dfa_states]:
                        key = (frozenset(dfa_table[dfa_states]), alpha)
                    if key not in dfa_table:
                        states.add(frozenset(dfa_table[dfa_states]))
                        x = 1
                        dfa_table[key] = []

        return FiniteAutomaton(initial_state=init_state, alphabet=self.alphabet, states=states, transitions=dfa_table)

    def __str__(self):
        dfa_str = "States: {}\n".format(self.states)
        dfa_str += "Alphabet: {}\n".format(self.alphabet)
        dfa_str += "Transitions:\n"
        for (source, target), destination in self.transitions.items():
            dfa_str += "{} --{}--> {}\n".format(source, target, destination)
        dfa_str += "Initial State: {}\n".format(self.initial_state)
        dfa_str += "Final States: {}\n".format(self.final_states)
        return dfa_str
