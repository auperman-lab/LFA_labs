class Grammar:

    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P

    def __str__(self):
        productions = "\n".join(f"{symbol} -> {', '.join(productions)}" for symbol, productions in self.P.items())
        return f"\nNon-terminals (VN): {self.VN}\nTerminals (VT): {self.VT}\nProductions (P):\n{productions}"
