class Grammar:

    # Variant 12:
    # VN={S, F, D},
    # VT={a, b, c},
    # P={
    #     S → aF
    #     F → bF
    #     F → cD
    #     S → bS
    #     D → cS
    #     D → a
    #     F → a
    # }

    # Variant 12
    # Q = {q0, q1, q2, q3},
    # ∑ = {a, b, c},
    # F = {q2},
    # δ(q0, b) = q0,
    # δ(q0, a) = q1,
    # δ(q1, c) = q1,
    # δ(q1, a) = q2,
    # δ(q3, a) = q1,
    # δ(q3, a) = q3,
    # δ(q2, a) = q3.

    # def __init__(self):
    #     self.VN = {'S', 'F', 'D'}
    #     self.VT = {'a', 'b', 'c'}
    #     self.P = {
    #         'S': ['aF', 'bS', 'aS'],
    #         'F': ['bF', 'cD', 'a'],
    #         'D': ['cS', 'a'],
    #     }

    def __init__(self):
        self.VN = {'S', 'A', 'B', 'C'}
        self.VT = {'a', 'b', 'c'}
        self.F = {'B'}
        self.P = {
            'S': ['bS', 'aA'],
            'A': ['cA', 'aB'],
            'B': ['aC'],
            'C': ['aC', 'aA'],
        }

    def print_grammar(self):
        print("Non-terminals (VN):", self.VN)
        print("Terminals (VT):", self.VT)
        print("Productions (P):")
        for symbol, productions in self.P.items():
            print(symbol, "->", ", ".join(productions))

    def check_dfa_or_nfa(self):
        is_dfa = True
        for symbol in self.VN:
            transitions = {}
            for production in self.P[symbol]:
                if production[0] in transitions:
                    is_dfa = False
                    break
                transitions[production[0]] = production[1:]
        return "DFA" if is_dfa else "NFA"

    def chomsky_classification(self):
        isRegular = True
        isContextFree = True
        isContextSensitive = True
        isRightRegular = False
        isLeftRegular = False
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                if rhs[0] in self.VN and all(symbol in self.VT for symbol in rhs[1:]):
                    isRightRegular = True

                if rhs[-1] in self.VN and all(symbol in self.VT for symbol in rhs[:-1]):
                    isLeftRegular = True

                # Check for Type 3 (Regular Grammar)
                if not (len(rhs) == 1 and rhs in self.VT) and not (isRightRegular ^ isLeftRegular):
                    isRegular = False

                # Check for Type 2 (Context-Free Grammar)
                if len(lhs) > 1 or all(symbol in self.VT for symbol in lhs):
                    isContextFree = False

                # Check for Type 1 (Context-Sensitive Grammar)
                if len(rhs) < len(lhs):
                    isContextSensitive = False

        if isRegular:
            return "Type 3: Regular Grammar"
        elif isContextFree:
            return "Type 2: Context-Free Grammar"
        elif isContextSensitive:
            return "Type 1: Context-Sensitive Grammar"
        else:
            return "Type 0: Unrestricted Grammar"
