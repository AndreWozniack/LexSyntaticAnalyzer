from Token import Token

def parse_number(line: str, start_index: int) -> tuple[str, str, int]:
    i = start_index
    has_dot = False
    if line[i] == '-':
        i += 1

    while i < len(line) and (line[i].isdigit() or (line[i] == '.' and not has_dot)):
        if line[i] == '.':
            has_dot = True
        i += 1

    value = line[start_index:i]
    token_class = "REAL_NUMBER" if has_dot else "INTEGER_NUMBER"
    return value, token_class, i


def tokenizeLine(line: str, lineNumber: int) -> list[Token]:
    tokens = []
    i = 0

    operatorsList = ["+", "-", "*", "/", "^", "%", "|"]
    keywordsList = ["RES", "MEM", "IF", "THEN", "ELSE", "FOR"]

    while i < len(line):
        char = line[i]

        if char.isspace():
            i += 1
            continue

        if char == "(":
            tokens.append(Token("(", "LEFT_PARENTHESIS", lineNumber, i + 1))
            i += 1
            continue

        elif char == ")":
            tokens.append(Token(")", "RIGHT_PARENTHESIS", lineNumber, i + 1))
            i += 1
            continue

        if char == '-' and (
                i + 1 < len(line) and line[i + 1].isdigit() and
                (i == 0 or line[i - 1] in " (")
        ):
            value, token_class, new_i = parse_number(line, i)
            tokens.append(Token(value, token_class, lineNumber, i + 1))
            i = new_i
            continue

        if char.isdigit():
            value, token_class, new_i = parse_number(line, i)
            tokens.append(Token(value, token_class, lineNumber, i + 1))
            i = new_i
            continue

        if char in operatorsList:
            tokens.append(Token(char, "OPERATOR", lineNumber, i + 1))
            i += 1
            continue

        if char.isalpha():
            start_index = i
            while i < len(line) and (line[i].isalnum() or line[i] == "_"):
                i += 1

            value = line[start_index:i]
            upper_value = value.upper()

            if upper_value in keywordsList:
                token_class = "KEYWORD"
            else:
                token_class = "IDENTIFIER"

            tokens.append(Token(value, token_class, lineNumber, start_index + 1))
            continue

        raise ValueError(f"Unexpected character '{char}' at line {lineNumber}, column {i + 1}")

    return tokens