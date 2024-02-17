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
                    self.transitions[(symbol, production)] = 'final'
                else:
                    self.transitions[(symbol, production[0])] = production[1]

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
