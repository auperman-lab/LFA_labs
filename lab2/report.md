# Laboratory Work Report


## Legend

- [Objectives](#objectives)
- [Implementation](#implementation)
  - [Finite Automaton Characteristics](#characteristics-of-an-automaton)
  - [Project Setup](#project-setup)
  - [Finite Automaton to Regular Grammar](#finite-automaton-to-a-regular-grammar)
  - [NDFA/DFA Classification](#determine-ndfa-or-dfa)
  - [NDFA to DFA Conversion](#ndfa-to-dfa-conversion)
  - [Graph Visualisation](#graphical-representation)
  - [Results](#results)
- [Conclusion](#conclusion)

<br><br>
<br><br>
<br><br>

## Objectives

1. **Understand what an automaton is and what it can be used for**:
   - Discover what a automaton is and what it needs to have in order to be considered a formal one.

2. **Continuing the work in the same repository and the same project, the following need to be added**:
   - Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy
   - For this you can use the variant from the previous lab.
  

3. **According to your variant number, get the finite automaton definition and do the following tasks**:
   - Implement conversion of a finite automaton to a regular grammar.
   - Determine whether your FA is deterministic or non-deterministic.
   - Implement some functionality that would convert an NDFA to a DFA.
   - Represent the finite automaton graphically (Optional, and can be considered as a bonus point)
     - You can use external libraries, tools or APIs to generate the figures/diagrams.
     - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.


## Implementation


### Characteristics of an Automaton:
**States**: An automaton consists of a finite set of states. These states represent different configurations or conditions of the system being modeled.

**Transitions**: There are transitions between states based on inputs. These transitions are defined by a transition function, which determines the next state of the automaton given the current state and input symbol.

**Alphabet**: An alphabet is a finite set of symbols that the automaton recognizes or operates on. Inputs to the automaton are drawn from this alphabet.

**Accepting States (Final States)**: In some types of automata, there are specific states called accepting states or final states. When the automaton reaches one of these states after processing a sequence of inputs, it accepts the input sequence.

**Initial State**: The automaton starts its operation from a specific initial state. This state represents the starting configuration of the system.

**Deterministic or Non-deterministic Behavior**: An automaton can be deterministic, where for each state and input symbol, there is exactly one possible transition, or non-deterministic, where multiple transitions may be possible for the same state and input symbol.

**Acceptance Criteria**: Depending on the type of automaton, the acceptance criteria may vary. For example, in a deterministic finite automaton (DFA), acceptance is determined solely by whether the final state is an accepting state, whereas in a non-deterministic finite automaton (NFA), acceptance can be based on multiple possible paths through the automaton.


### Project Setup

#### Chomsky hierarchy

```python
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

```


**Right-Regular Grammar Check:**

  - if rhs[0] in self.VN and all(symbol in self.VT for symbol in rhs[1:]):
    - This condition checks if the right-hand side of the production rule (rhs) is a right-regular grammar by ensuring:
      - The first symbol (rhs[0]) is a non-terminal (VN).
      - All remaining symbols in the right-hand side (rhs[1:]) are terminals (VT).
  - If this condition is met, isRightRegular flag is set to True.

**Left-Regular Grammar Check:**

- if rhs[-1] in self.VN and all(symbol in self.VT for symbol in rhs[:-1]):
  - This condition checks if the right-hand side of the production rule (rhs) is a left-regular grammar by ensuring:
    - The last symbol (rhs[-1]) is a non-terminal (VN).
    - All symbols except the last one in the right-hand side (rhs[:-1]) are terminals (VT).
  - If this condition is met, isLeftRegular flag is set to True.

**Regular Grammar Check (Type 3):**

- if not (len(rhs) == 1 and rhs in self.VT) and not (isRightRegular ^ isLeftRegular):
  - This condition checks if the production rule (rhs) satisfies the conditions for a regular grammar by ensuring:
    - The right-hand side (rhs) is not a single terminal symbol.
    - It's neither purely right-regular nor purely left-regular (i.e., XOR condition).
  - If this condition is not met, isRegular flag is set to False, indicating that the grammar is not a regular grammar.

**Context-Free Grammar Check (Type 2):**

- if len(lhs) > 1 or all(symbol in self.VT for symbol in lhs):
  - This condition checks if the left-hand side of the production rule (lhs) satisfies the conditions for a context-free grammar by ensuring:
    - The left-hand side consists of only one non-terminal symbol.
    - All symbols in the left-hand side (lhs) are terminals (VT).
  - If this condition is not met, isContextFree flag is set to False, indicating that the grammar is not a context-free grammar.

**Context-Sensitive Grammar Check (Type 1):**


- if len(rhs) < len(lhs):
  - This condition checks if the production rule (rhs) satisfies the conditions for a context-sensitive grammar by ensuring:
    - The length of the right-hand side (rhs) is less than the length of the left-hand side (lhs).
  - If this condition is not met, isContextSensitive flag is set to False, indicating that the grammar is not a context-sensitive grammar.

**Unrestricted Grammar**
- If no grammar doesnt respect the rules above it is Unrestricted Grammar.

### Finite Automaton Implementation

For the Finite Automaton implementation, there is a Python class [Finite Automaton](grammar.py) to represent the grammar.


#### Finite Automaton to a Regular Grammar


```python
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
```


This Python code defines a method that converts a given finite automaton into an equivalent regular grammar. It maps states to non-terminal symbols, transitions to production rules, and final states are preserved.
#### Determine NDFA or DFA

```python
    def check_dfa_or_nfa(self):
        is_dfa = True

        for qwer, trans in self.transitions.items():
            if len(trans) > 1:
                is_dfa = False
                break

        return "DFA" if is_dfa else "NFA"
```

This Python method determines if a given finite automaton is a deterministic finite automaton (DFA) or a nondeterministic finite automaton (NFA) by checking if any state has more than one transition.

#### NDFA to DFA Conversion

```python
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
```

This Python method converts a nondeterministic finite automaton (NFA) into a deterministic finite automaton (DFA). It starts with the initial state of the NFA and constructs a DFA transition table, considering all possible combinations of states and alphabet symbols. It iteratively computes transitions for each state set based on the NFA's transitions, updating the DFA table accordingly. This process continues until no new transitions can be added. It identifies final states by checking if any state in a DFA state set corresponds to a final state in the NFA. Finally, it returns a new DFA representation, effectively capturing the behavior of the original NFA in a deterministic manner.

#### Graphical Representation

```python
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

```

This Python method utilizes the Graphviz library to visualize a finite automaton (FA). It creates nodes for each state, distinguishing final states, and edges for transitions between states, producing a PNG image named 'finite_automaton.png'.


### Results 

```text
Chomsky Classification: Type 3: Regular Grammar


FA to grammar
Non-terminals (VN): {'S', 'A', 'B', 'C'}
Terminals (VT): {'a', 'b', 'c'}
Productions (P):
S -> bS, aA
A -> cA, aB
B -> aC
C -> aC, aA


DFA or NFA :  NFA
NFA after conversion :
States: {frozenset({'B'}), frozenset({'A', 'C'}), frozenset({'B', 'A', 'C'}), 'S', frozenset({'A'}), frozenset({'C'})}
Alphabet: {'a', 'b', 'c'}
Transitions:
frozenset({'S'}) --a--> frozenset({'A'})
frozenset({'S'}) --b--> frozenset({'S'})
frozenset({'S'}) --c--> frozenset()
frozenset({'A'}) --a--> frozenset({'B'})
frozenset({'A'}) --b--> frozenset()
frozenset({'A'}) --c--> frozenset({'A'})
frozenset({'B'}) --a--> frozenset({'C'})
frozenset({'B'}) --b--> frozenset()
frozenset({'B'}) --c--> frozenset()
frozenset({'C'}) --a--> frozenset({'A', 'C'})
frozenset({'C'}) --b--> frozenset()
frozenset({'C'}) --c--> frozenset()
frozenset({'A', 'C'}) --a--> frozenset({'B', 'A', 'C'})
frozenset({'A', 'C'}) --b--> frozenset()
frozenset({'A', 'C'}) --c--> frozenset({'A'})
frozenset({'B', 'A', 'C'}) --a--> frozenset({'B', 'A', 'C'})
frozenset({'B', 'A', 'C'}) --b--> frozenset()
frozenset({'B', 'A', 'C'}) --c--> frozenset({'A'})
Initial State: S
Final States: {frozenset({'B', 'A', 'C'}), frozenset({'B'})}


```


## Conclusion

In conclusion, this lab presented a comprehensive exploration of finite automata, covering various essential operations and transformations. Beginning with the conversion of finite automata to regular grammars, the lab showcased methods for distinguishing deterministic and nondeterministic finite automata, crucial for understanding their computational power and complexity. The conversion from nondeterministic to deterministic finite automata provided valuable insight into the practical implications of automata theory, demonstrating how to efficiently represent complex systems using deterministic models. Furthermore, the visualization of finite automata using Graphviz offered a visually intuitive perspective, aiding in the comprehension and analysis of automaton structures and behaviors. Overall, through practical implementation and visualization techniques, this lab effectively reinforced fundamental concepts in automata theory, enhancing understanding and proficiency in the realm of formal languages and automata.