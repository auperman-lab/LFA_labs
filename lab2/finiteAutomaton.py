import graphviz

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
                self.transitions.setdefault((symbol, production[0]), []).append(production[1])

        self.initial_state = 'S'
        self.final_states = grammar.F

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

        regular_grammar.VN = self.states
        regular_grammar.VT = self.alphabet

        regular_grammar.P = {}

        for (source, target), destination in self.transitions.items():
            for item in destination:
                regular_grammar.P.setdefault(source, []).append(target + item)

        regular_grammar.F = self.final_states

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
        dfa_table = {(frozenset(init_state), alpha): set() for alpha in self.alphabet}
        states = set(init_state)
        final_states = set()
        x = 1
        while x != 0:
            x = 0
            keys_to_process = [key for key, value in dfa_table.items() if value == set()]

            for dfa_states in keys_to_process:
                symbol = dfa_states[1]
                for state in dfa_states[0]:
                    transitions_for_state = self.transitions.get((state, symbol), [])
                    dfa_table[dfa_states].update(transitions_for_state)

                for alpha in self.alphabet:
                    key = (frozenset(dfa_table[dfa_states]), alpha)
                    if key not in dfa_table and dfa_table[dfa_states] != set():
                        states.add(frozenset(dfa_table[dfa_states]))
                        x = 1
                        dfa_table[key] = set()

        for item in dfa_table:
            for state in item[0]:
                if state in self.final_states:
                    final_states.add(item[0])
            dfa_table[item] = frozenset(dfa_table[item])

        return FiniteAutomaton(initial_state=init_state, alphabet=self.alphabet, states=states, transitions=dfa_table, final_states=final_states)

    def __str__(self):
        dfa_str = "States: {}\n".format(self.states)
        dfa_str += "Alphabet: {}\n".format(self.alphabet)
        dfa_str += "Transitions:\n"
        for (source, target), destination in self.transitions.items():
            dfa_str += "{} --{}--> {}\n".format(source, target, destination)
        dfa_str += "Initial State: {}\n".format(self.initial_state)
        dfa_str += "Final States: {}\n".format(self.final_states)
        return dfa_str

    def draw(self):
        dot = graphviz.Digraph(comment='Finite Automaton')

        for state in self.states:
            if state in self.final_states:
                dot.node(str(set(state)), shape='doublecircle')
            else:
                dot.node(str(set(state)), shape='circle')

        for transition, to_state in self.transitions.items():
            from_state, symbol = transition
            if isinstance(to_state, list):
                for state in to_state:
                    dot.edge(str(set(from_state)), str(set(state)), label=symbol)
            else:
                dot.edge(str(set(from_state)), str(set(to_state)), label=symbol)

        dot.render('finite_automaton', format='png', cleanup=True)
        print("Automaton visualization saved as 'finite_automaton.png'")
