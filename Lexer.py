from TokenType import *
from Token import *

class Lexer:
    def __init__(self, line: str, line_number: int):
        self.line = line
        self.line_number = line_number
        self.index = 0
        self.tokens = []
        self.operators = ("+", "-", "*", "/", "%", "|", "^")
        self.keywords = (
            "MEM",
            "RES",
            "IF",
            "THEN",
            "ELSE",
            "FOR"
        )


    def current_char(self):
        return self.line[self.index] if self.index < len(self.line) else None

    def advance(self):
        self.index += 1

    def add_operator_token(self):
        value = self.current_char()
        self.tokens.append(Token(value, TokenType.OPERATOR, self.line_number, self.index))

    def is_negative_number(self):
        return self.current_char() == '-' and self.peek() and (self.peek().isdigit() or self.peek() == '.')

    def peek(self):
        return self.line[self.index + 1] if self.index + 1 < len(self.line) else None

    def operators(self):
        if self.current_char() == "-":
            self.number()

    def number(self):
        start = self.index
        has_dot = False

        if self.current_char() == '-':
            self.advance()

        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break  # segundo ponto, erro
                has_dot = True
            self.advance()

        value = self.line[start:self.index]
        token_type = TokenType.REAL_NUMBER if has_dot else TokenType.INTEGER_NUMBER
        self.tokens.append(Token(value, token_type, self.line_number, start))

    def keyword(self):
        start = self.index
        while self.current_char() and self.current_char().isalpha():
            self.advance()

        value = self.line[start:self.index].upper()
        if value in self.keywords:
            token_type = TokenType.KEYWORD
        else:
            raise Exception(f"Unrecognized keyword: {value} at index {self.index} in line {self.line_number}")

        self.tokens.append(Token(value, token_type, self.line_number, start))


    def tokenize(self):
        while self.index < len(self.line):
            char = self.current_char()

            if char.isspace():
                self.advance()
                continue

            if self.is_negative_number():
                self.number()

            elif char.isdigit():
                self.number()

            elif char in self.operators:
                self.add_operator_token()
                self.advance()

            elif char == '(':
                self.tokens.append(Token(self.current_char(), TokenType.LEFT_PARENTHESIS, self.line_number, self.index))
                self.advance()

            elif char == ')':
                self.tokens.append(Token(self.current_char(), TokenType.RIGHT_PARENTHESIS, self.line_number, self.index))
                self.advance()

            if char.isalpha():
                self.keyword()

        return self.tokens