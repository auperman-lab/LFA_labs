# Laboratory Work Report


## Legend

- [Objectives](#objectives)
- [Implementation](#implementation)
  - [Formal Languages](#characteristics-of-formal-languages)
  - [Project Setup](#project-setup)
  - [Grammars](#grammar-class-implementation)
  - [Finite Automaton](#finite-automaton-implementation)
  - [Results](#results)
- [Conclusion](#conclusion)

<br><br>
<br><br>
<br><br>

## Objectives

1. **Understanding Formal Languages**:
   - Discover what a language is and what it needs to have in order to be considered a formal one.

2. **Project Setup**:
   - Provide the initial setup for the evolving project to be worked on during this semester.
   - Create a GitHub repository for storing and updating the project.
   - Choose a programming language, prioritizing simplicity in problem-solving.
   - Store reports separately to simplify verification of work.

3. **Grammar Implementation**:
   - Implement a type/class for the grammar.
   - Add a function to generate 5 valid strings from the language expressed by the grammar.

4. **Finite Automaton Conversion**:
   - Implement functionality to convert an object of type Grammar to one of type Finite Automaton.
   - Add a method to the Finite Automaton class to check if an input string can be obtained via state transition from it.


## Implementation


### Characteristics of Formal Languages:
**Alphabet**: A finite set of symbols from which strings are formed. It represents the basic building blocks of the language.

**Strings**: A sequence of symbols from the alphabet. These strings are the elements of the language.

**Syntax**: The rules that govern how strings are formed from the alphabet. Syntax defines the structure and composition of valid strings.

**Semantics**: The meaning associated with strings in the language. Semantics determines the interpretation or behavior of valid strings.

**Formal Grammar**: A set of rules for generating valid strings in the language. Formal grammars categorize languages into different classes based on their expressive power.

**Automata Theory**: Mathematical models used to recognize or generate strings in a language. Automata, such as finite automata and pushdown automata, provide theoretical frameworks for studying formal languages.

Formal languages play a crucial role in various areas of computer science, including compiler design, natural language processing, and cryptography. Understanding formal languages is fundamental for developing computational solutions and analyzing algorithms.


### Project Setup

To kickstart the evolving project for this semester, I completed the initial setup as follows:

#### GitHub Repository Creation

- Created a GitHub repository named "Semester_Project" to manage and track the progress of the project.
- Initialized the repository with a README file to provide an overview of the project.

#### Programming Language Selection

- Chose Python as the programming language for the project due to its simplicity, readability, and extensive libraries.
- Python offers robust support for various tasks, making it suitable for solving the problems at hand efficiently.

#### Separation of Reports

- Established a clear structure for storing reports separately from the project code.
- Each laboratory work report will be stored in its own markdown (.md) file within the repository.

### Grammar Implementation

For the grammar implementation, I created a Python class [Grammar](grammar.py) to represent the grammar and added a [String Generator Method](main.py)  to generate 5 valid strings from the language expressed by the grammar.


#### Grammar Class Implementation

```python
class Grammar:
    def __init__(self):
        self.VN = {'S', 'F', 'D'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aF', 'bS'],
            'F': ['bF', 'cD', 'a'],
            'D': ['cS', 'a'],
        }

```

In this code, I defined a class named Grammar to represent the grammar. It includes attributes for non-terminal symbols (VN), terminal symbols (VT), and production rules (P).

#### String Generator Method

```python

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

```

This method takes a grammar object and a number of strings (num_strings) as input and generates the specified number of valid strings based on the grammar. Each generated string is accompanied by a list of transitions used to derive that string.

### Finite Automaton implementation

For the Finite Automaton implementation, I created a Python class named [Finite Automaton](finiteAutomaton.py)
 to represent the finite automaton. This class includes methods to convert a grammar object to a finite automaton and to check if an input string can be obtained via state transition from it.



#### Transforming Grammar to Finite Automaton

```python
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
```

This method takes a grammar object as input and converts it to a finite automaton. It sets the states, alphabet, transitions, initial state, and final states of the finite automaton based on the grammar provided.

#### Method for checking input string

```python
   def check_string(self, input_string):

        current_state = self.initial_state

        for char in input_string:
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)]
            else:
                return False

        return True
```

This method check_string takes an input string and checks if it can be obtained via state transition from the finite automaton. It iterates through each character of the input string, updating the current state based on the transitions defined in the automaton. If the final state is reached after processing the entire input string, the method returns True indicating that the string is accepted by the automaton. Otherwise, it returns False.

#### Results 

```text
Generated strings:
-> S -> aF -> a -> aa 

-> S -> bS -> aF -> cD -> cS -> bS -> aF -> bF -> cD -> a -> baccbabca 

-> S -> bS -> aF -> a -> baa 

-> S -> aF -> cD -> cS -> aF -> bF -> bF -> bF -> a -> accabbba 

-> S -> bS -> bS -> aF -> bF -> bF -> a -> bbabba 


Checking if input strings can be created with actual Grammar:
'baca' can be created with actual Grammar
'aa' can be created with actual Grammar
'dawada' can't be created with actual Grammar
'aaba' can't be created with actual Grammar
'babca' can be created with actual Grammar

```


## Conclusion

In this lab, I explored formal languages, grammars, and finite automata. I learned about the components of a formal language, including alphabets, strings, syntax, and semantics.

For project setup, I created a GitHub repository, selected Python for its simplicity, and organized reports separately for clarity.

Implementing a grammar class in Python allowed me to generate valid strings from the language expressed by the grammar. Additionally, I developed a Finite Automaton class to convert a grammar object and check input strings for acceptance.

This lab provided valuable insights into formal languages and their practical implementation in Python. It sets a strong foundation for future exploration in computer science projects.