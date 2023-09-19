from Symbol import Symbol

class Token:
    def __init__(self, lexeme, symbol, line, column):
        self.lexeme = lexeme
        self.symbol = symbol
        self.line = line
        self.column = column
        self.lexeme_index = None

    def __repr__(self):
        return f"[{self.lexeme_index}, {self.symbol}, {self.lexeme}, ({self.line}, {self.column})]"
