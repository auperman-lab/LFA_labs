from collections import deque

from lab2.grammar import Grammar


class FiniteAutomaton:
    def __init__(self, grammar):

        self.states = {}
        self.alphabet = {}
        self.transitions = {}
        self.initial_state = None
        self.final_states = {}

        self.convert_from_grammar(grammar)

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
        dfa = FiniteAutomaton(Grammar())
        visited = set()
        queue = deque([frozenset([self.initial_state])])

        while queue:
            current_states = queue.popleft()
            if current_states in visited:
                continue
            visited.add(current_states)

            for symbol in self.alphabet:
                next_states = set()
                for state in current_states:
                    if (state, symbol) in self.transitions:
                        next_states.update(set(self.transitions[(state, symbol)]))
                if next_states:
                    dfa.transitions[(current_states, symbol)] = next_states
                    queue.append(frozenset(next_states))
                    if any(state in self.final_states for state in next_states):
                        dfa.final_states.add(frozenset(next_states))
        return dfa

    def __str__(self):
        dfa_str = "States: {}\n".format(self.states)
        dfa_str += "Alphabet: {}\n".format(self.alphabet)
        dfa_str += "Transitions:\n"
        for (source, target), destination in self.transitions.items():
            dfa_str += "{} --{}--> {}\n".format(source, target, destination)
        dfa_str += "Initial State: {}\n".format(self.initial_state)
        dfa_str += "Final States: {}\n".format(self.final_states)
        return dfa_str