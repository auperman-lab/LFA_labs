# Laboratory Work Report


## Legend

- [Objectives](#objectives)
- [Implementation](#implementation)
  - [Lexical Analysis](#lexical-analysis)
  - [Lexer/Scaner/Tokenizer](#lexerscannertokenizer)
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

1. **Understand what lexical analysis [1] is**

2. **Get familiar with the inner workings of a lexer/scanner/tokenizer.**

3. **Implement a sample lexer and show how it works.**
 

## Implementation


### Lexical Analysis:

Lexical analysis, often referred to as lexing, is the initial phase of the compilation process in computer science. It's responsible for breaking down the input source code into a sequence of tokens or lexemes, which are the smallest units of meaning in a programming language. These tokens serve as the basic building blocks for further processing by the compiler or interpreter.


**Tokenization**: Lexical analysis involves scanning the source code character by character and grouping them into meaningful tokens based on the language's syntax rules. These tokens can include identifiers (variable names, function names), keywords (reserved words in the language), literals (constants like numbers or strings), operators, and punctuation symbols.

**Ignoring Whitespace and Comments**: During lexical analysis, whitespace characters (spaces, tabs, newline characters) are typically ignored, as they usually do not affect the meaning of the code. Similarly, comments (lines of text intended for human readers and not executed by the program) are also skipped.

**Error Handling**: Lexical analysis also involves detecting and handling lexical errors, such as invalid characters or tokens that don't conform to the language's syntax rules. When an error is encountered, the lexer may report the error and possibly recover to continue processing the input.

**Output**: The output of lexical analysis is a stream of tokens, which is passed on to the next phase of the compilation process, known as parsing. Parsing involves analyzing the structure of the tokens according to the grammar of the programming language.

Overall, lexical analysis plays a crucial role in the compilation process by transforming raw source code into a form that can be easily processed by subsequent stages of the compiler or interpreter. It lays the foundation for understanding the structure and meaning of the code, facilitating further analysis and translation into machine-readable form.

### Lexer/Scanner/Tokenizer

To get familiar with the inner workings of a lexer/scanner/tokenizer, it's essential to understand its core functionalities and how it processes input source code. Here's an overview of the inner workings:

**Input Buffering**: The lexer reads characters from the input source code file or string one at a time. It may use techniques such as buffering to efficiently manage input data.

**Token Recognition**: As the lexer reads characters, it identifies patterns in the input that match predefined token types defined by the language's grammar. These patterns may include keywords, identifiers, literals, operators, and punctuation symbols.

**Lexical Analysis Rules**: The lexer applies lexical analysis rules defined by the language's specification to determine how to recognize and categorize tokens. These rules typically include regular expressions or finite automata that define the syntax of the language.

**Token Generation**: Once a token is recognized, the lexer generates a token object representing the token type and its associated value (if applicable). This token object typically contains information such as the token type, lexeme (the actual text of the token), line number, and column number.

**Error Handling**: The lexer may detect lexical errors, such as invalid characters or tokens that do not conform to the language's syntax rules. It reports these errors and may attempt to recover to continue processing the input.

**Whitespace and Comments**: The lexer typically ignores whitespace characters (spaces, tabs, newline characters) and comments during tokenization, as they usually do not affect the meaning of the code.

**Token Output**: As tokens are generated, the lexer outputs them to the parser or another component of the compiler or interpreter for further processing. The parser uses these tokens to build the abstract syntax tree (AST) representing the structure of the source code.

**Efficiency and Optimization**: Lexers may employ various optimization techniques to improve performance, such as token caching, lookahead, and minimizing memory usage.


### LEXER Implementation



#### Main Funnction:
For the Lexer implementation, there is a Python file [Main](main.py) to start the important parts of the lexer.


```python
while True:
    try:
        text = input("graph> ")
        lexer = Lexer(text)
        tokens = lexer.generate_tokens()
        parser = Parser(tokens)
        tree = parser.parse()
        # print(tree)
        if not tree:
            continue
        interpreter = Interpreter()
        graph = interpreter.visit(tree)
        graph.draw()
    except Exception as e:
        print(e)

```
This Python main function creates an interactive graph processing system. It continuously prompts the user for graph commands, which are then tokenized, parsed, interpreted, and finally, the resulting graph is visualized. If any errors occur during this process, they are printed to the console.


#### Tokens

This code defines an enumeration `TokenType` and a data class `Token` to represent token types and values, facilitating lexical analysis in language processing. It is located inside [tokens.py](tokens.py)

```python
class TokenType(Enum):
    DASH = 0
    NAME = 1
    LEFT = 2
    RIGHT = 3
    FINAL = 4
    WEIGHT = 5
```


#### Lexer
The Lexer class tokenizes input text into tokens like DASH, LEFT, RIGHT, NAME, WEIGHT, and FINAL based on predefined rules. It's a crucial step in language processing. This class is located inn [Lexer](lexer.py)
```python

 def generate_tokens(self):
        while self.current_char is not None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.DASH)
            elif self.current_char in ALPHA:
                yield self.generate_name()
            elif self.current_char == '<':
                self.advance()
                yield Token(TokenType.LEFT)
            elif self.current_char == '>':
                self.advance()
                yield Token(TokenType.RIGHT)
            elif self.current_char == '.' or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == '*':
                self.advance()
                yield Token(TokenType.FINAL)
            else:
                raise Exception(f"Illegal character '{self.current_char}'")


```

Here is the hearth of this class , generate_tokens method , which categorize input into tokens. Also names and number are categorized in separate methods for readability. 


### Results 

```text
graph> a<-->b
ConnectNode(NameNode(value='a', status='not final') <- 0 -> NameNode(value='b', status='not final'))
graph> a-8-n
ConnectNode(NameNode(value='a', status='not final') - 8.0 - NameNode(value='n', status='not final'))
graph> 
```


## Conclusion


This laboratory work delved into the fundamentals of lexical analysis, the functioning of a lexer/scanner/tokenizer, and its practical implementation in Python. Understanding lexical analysis is pivotal in breaking down source code into tokens, forming the groundwork for subsequent language processing stages.

The implementation of a Lexer class demonstrated tokenization, recognizing patterns, and handling errors according to predefined rules. The main function showcased an interactive graph processing system, where user-inputted commands were tokenized, parsed, interpreted, and visualized as a graph representation. This integration illustrated the seamless flow from lexical analysis to visualization in language processing.

By comprehending lexical analysis principles and witnessing their application through hands-on implementation, we gained insights into the intricate workings of language processing systems. This laboratory work fostered a deeper understanding of lexer functionality and its role in language interpretation and compilation processes, providing valuable practical experience in language processing concepts.
