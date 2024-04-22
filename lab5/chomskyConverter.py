from lab5.grammar import Grammar


class ChomskyConverter:

    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P

    def convert(self):
        self.epsilonElimination()
        grammar = Grammar(self.VN, self.VT, self.P)
        print('\nafter eliminating epsilon')
        print(grammar)

        self.nonproductiveElimination()
        grammar = Grammar(self.VN, self.VT, self.P)
        print('\nafter eliminating nonproductive symbols')
        print(grammar)

        self.nonproductiveElimination()
        grammar = Grammar(self.VN, self.VT, self.P)
        print('\nafter eliminating inaccessible symbols')
        print(grammar)

        print("\nafter eliminating any renaming")
        self.renamingElimination()
        grammar = Grammar(self.VN, self.VT, self.P)
        print(grammar)

        print("\n after chomsky transformation")
        self.chomskyStep()
        grammar = Grammar(self.VN, self.VT, self.P)

        return grammar

    def epsilonElimination(self):
        counter = 1
        while counter:
            for symbol in self.P:
                for production in list(self.P[symbol]):
                    if production == '':
                        self.symbolReplacement(symbol)
                        self.P[symbol].remove('')
                        counter += 1
            counter -= 1

    def symbolReplacement(self, char):
        for symbol1 in list(self.P):
            for production1 in list(self.P[symbol1]):
                if char in production1:
                    sp = [i for i in range(len(production1)) if production1[i] == char]
                    new_productions = []
                    for i in range(len(sp)):
                        new_productions.append(production1[:sp[i]] + production1[sp[i] + 1:])
                        for j in range(i + 1, len(sp)):
                            new_productions.append(
                                production1[:sp[i]] + production1[sp[i] + 1:sp[j]] + production1[sp[j] + 1:])

                    new_productions.append(production1.replace(char, ''))
                    for np in new_productions:
                        self.P[symbol1].add(np)

    def renamingElimination(self):
        counter = 1
        while counter:
            for symbol in self.P:
                for production in list(self.P[symbol]):
                    if production in self.VN:
                        self.P[symbol].remove(production)
                        for relation in self.P[production]:
                            self.P[symbol].add(relation)
                            counter += 1
            counter -= 1

    def nonproductiveElimination(self):
        counter = 1
        while counter:
            for symbol in list(self.P):
                dzone = False
                for production in list(self.P[symbol]):
                    terminals = False
                    nterminals = False
                    itself = False
                    for p in production:
                        if p == symbol:
                            itself = True
                        elif p in self.VN:
                            nterminals = True
                        elif p in self.VT:
                            terminals = True

                    if itself and not nterminals:
                        dzone = True
                    if (terminals or nterminals) and not itself:
                        dzone = False
                        break
                if dzone:
                    self.VN.remove(symbol)
                    del self.P[symbol]

                    self.eliminateSymbol(symbol)
                    counter += 1

            counter -= 1

    def eliminateSymbol(self, char):
        for symbol in self.P:
            for production in list(self.P[symbol]):
                if char in production:
                    self.P[symbol].add(production.replace(char, ''))
                    self.P[symbol].remove(production)
                    self.P[symbol].remove('')

    def inaccessibleElimination(self):
        counter = 1
        while counter:
            production_w_start = self.remove_key(self.P, 'S')
            for symbol in list(production_w_start):
                production_w_symbol = self.remove_key(self.P, symbol)
                accessible = False

                for symbols in list(production_w_symbol):
                    for production in symbols:
                        if symbol in production:
                            accessible = True
                            break

                    if accessible:
                        break

                if not accessible:
                    self.VN.remove(symbol)
                    del self.P[symbol]
                    counter += 1

            counter -= 1

    def chomskyStep(self):
        for i, symbol in enumerate(self.VT):
            self.VN.add(f'X{i}')
            self.P[f'X{i}'] = symbol

        for symbol in list(self.P):
            for production in list(self.P[symbol]):
                if len(production) == 2:
                    new_production = ''
                    for char in production:
                        if char in self.VT:
                            newX = f'X{list(self.VT).index(char)}'
                            new_production += newX
                        else:
                            new_production += char
                    self.P[symbol].remove(production)
                    self.P[symbol].add(new_production)

    @staticmethod
    def remove_key(dictionary, key_to_remove):
        return {key: value for key, value in dictionary.items() if key != key_to_remove}
