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

    def __init__(self):
        self.VN = {'S', 'F', 'D'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aF', 'bS'],
            'F': ['bF', 'cD', 'a'],
            'D': ['cS', 'a'],
        }
