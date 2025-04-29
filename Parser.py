class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1

    def expect(self, expected_class: str):
        token = self.current()
        if token is None or token.token_class != expected_class:
            raise SyntaxError(
                f"Expected {expected_class}, found "
                f"'{token.value if token else 'EOF'}' at position {self.position}"
            )
        self.advance()
        return token

    def _parse_operand_then_operator_and_close(self):
        self.parse_expression()
        op = self.current()
        if not op or op.token_class != "OPERATOR":
            raise SyntaxError(
                f"Expected operator, found "
                f"'{op.value if op else 'EOF'}' at position {self.position}"
            )
        self.advance()
        self.expect("RIGHT_PARENTHESIS")

    def parse_expression(self):
        token = self.current()
        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token.token_class == "LEFT_PARENTHESIS":
            self.advance()
            first = self.current()

            # (MEM)
            if first.token_class == "KEYWORD" and first.value.upper() == "MEM":
                self.advance()
                self.expect("RIGHT_PARENTHESIS")
                return True

            # (V MEM) ou (N RES)
            if first.token_class in {"REAL_NUMBER", "INTEGER_NUMBER"}:
                self.advance()
                maybe_kw = self.current()
                if maybe_kw and maybe_kw.token_class == "KEYWORD" and maybe_kw.value.upper() in {"MEM", "RES"}:
                    self.advance()
                    self.expect("RIGHT_PARENTHESIS")
                    return True
                else:
                    # volta para parsing binário padrão
                    second = self.parse_expression()
                    op = self.current()
                    if not op or op.token_class != "OPERATOR":
                        raise SyntaxError(
                            f"Expected operator, found '{op.value if op else 'EOF'}' at position {self.position}"
                        )
                    self.advance()
                    self.expect("RIGHT_PARENTHESIS")
                    return True

            # parsing padrão (expr expr operador)
            first = self.parse_expression()
            second = self.parse_expression()
            op = self.current()
            if not op or op.token_class != "OPERATOR":
                raise SyntaxError(
                    f"Expected operator, found '{op.value if op else 'EOF'}' at position {self.position}"
                )
            self.advance()
            self.expect("RIGHT_PARENTHESIS")
            return True

        elif token.token_class in {"REAL_NUMBER", "INTEGER_NUMBER", "KEYWORD"}:
            self.advance()
            return True

        raise SyntaxError(
            f"Unexpected token '{token.value}' of type "
            f"{token.token_class} at position {self.position}"
        )

    def parse(self):
        self.parse_expression()
        if self.position != len(self.tokens):
            extra = self.tokens[self.position]
            raise SyntaxError(
                f"Unexpected extra token '{extra.value}' at end of input"
            )