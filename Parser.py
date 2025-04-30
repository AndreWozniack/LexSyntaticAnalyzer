class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1

    def expect(self, expected_class: str):
        """Verifica se o token atual é da classe esperada e avança"""
        token = self.current()
        if token is None or token.token_class != expected_class:
            raise SyntaxError(
                f"Expected {expected_class}, found "
                f"'{token.value if token else 'EOF'}' at position {self.position}"
            )
        self.advance()
        return token

    def parse(self):
        """Método principal de parsing que verifica a expressão e o fim da entrada"""
        self.parse_expression()
        if self.position != len(self.tokens):
            extra = self.tokens[self.position]
            raise SyntaxError(
                f"Unexpected extra token '{extra.value}' at end of input"
            )

    def parse_expression(self):
        """Analisa uma expressão e determina seu tipo"""
        token = self.current()
        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token.token_class == "LEFT_PARENTHESIS":
            return self.parse_parenthesized_expression()
        elif token.token_class in {"REAL_NUMBER", "INTEGER_NUMBER", "KEYWORD"}:
            return self.parse_atomic_value()
        else:
            raise SyntaxError(
                f"Unexpected token '{token.value}' of type "
                f"{token.token_class} at position {self.position}"
            )

    def parse_parenthesized_expression(self):
        self.advance()
        first = self.current()

        # Caso (MEM)
        if self.is_memory_access(first):
            return self.parse_memory_access()

        # Caso (número keyword)
        if first.token_class in {"REAL_NUMBER", "INTEGER_NUMBER"}:
            return self.parse_number_keyword_or_binary()

        # Caso expressão binária padrão
        return self.parse_standard_binary_expression()

    def is_memory_access(self, token):
        """Verifica se é um acesso à memória"""
        return token and token.token_class == "KEYWORD" and token.value.upper() == "MEM"

    def parse_memory_access(self):
        """Analisa uma expressão de acesso à memória (MEM)"""
        self.advance()  # Consome o token MEM
        self.expect("RIGHT_PARENTHESIS")
        return True

    def parse_number_keyword_or_binary(self):
        """Analisa uma expressão (número keyword) ou continua para binária"""
        self.advance()  # Consome o número
        maybe_kw = self.current()

        # Caso (V MEM) ou (N RES)
        if maybe_kw and maybe_kw.token_class == "KEYWORD" and maybe_kw.value.upper() in {"MEM", "RES"}:
            return self.parse_number_with_keyword()
        else:
            # Volta para parsing binário, já consumiu o primeiro operando
            return self.parse_binary_with_first_consumed()

    def parse_number_with_keyword(self):
        """Analisa uma expressão com número seguido de palavra-chave"""
        self.advance()  # Consome a keyword
        self.expect("RIGHT_PARENTHESIS")
        return True

    def parse_binary_with_first_consumed(self):
        """Analisa uma expressão binária onde o primeiro operando já foi consumido"""
        self.parse_expression()  # Analisa o segundo operando
        return self.parse_operator_and_close()

    def parse_standard_binary_expression(self):
        """Analisa uma expressão binária padrão (expr expr operador)"""
        self.parse_expression()  # Primeiro operando
        self.parse_expression()  # Segundo operando
        return self.parse_operator_and_close()

    def parse_operator_and_close(self):
        """Analisa um operador seguido de parêntese direito"""
        op = self.current()
        if not op or op.token_class != "OPERATOR":
            raise SyntaxError(
                f"Expected operator, found '{op.value if op else 'EOF'}' at position {self.position}"
            )
        self.advance()  # Consome o operador
        self.expect("RIGHT_PARENTHESIS")
        return True

    def parse_atomic_value(self):
        """Analisa um valor atômico (número ou palavra-chave)"""
        self.advance()  # Consome o token
        return True