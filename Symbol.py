from enum import Enum

class Symbol(Enum):
    ETX = 3
    LF = 10
    ASSIGNMENT = 11
    ADD = 21
    SUBTRACT = 22
    MULTIPLY = 23
    DIVIDE = 24
    MODULO = 25
    EQ = 31
    NE = 32
    GT = 33
    LT = 34
    GE = 35
    LE = 36
    VARIABLE = 41
    INTEGER = 51
    REM = 61
    INPUT = 62
    LET = 63
    PRINT = 64
    GOTO = 65
    IF = 66
    END = 67
    ERROR = 99  

