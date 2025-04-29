from dataclasses import dataclass

@dataclass
class Token:
    value: str
    token_class: str
    row: int
    column: int

    def __str__(self):
        return f"Token(value='{self.value}', token_class='{self.token_class}', row={self.row}, column={self.column})"