import sys
import re
from Symbol import Symbol
from Token import Token

number = 0
class LexicalAnalysis:
    def __init__(self):
        self.column = 0
        self.error = False
        self.lexeme = None
        self.line = 1
        self.source = None
        self.symbol_table = []
        self.tokens = []

    def print_tokens_and_symbols(self):
        #self.SyntaxAnalysis()
        
        print("\nTabela de símbolos :\n")
        symbol_table = self.get_symbol_table()
        print(symbol_table)
        print("\n Tokens :\n")
        print(self.tokens)


        print("\nFim das análises.")
        
    # Função para adicionar as palavras reservadas nos tokens
    def token_add(self, number, character, line, column):
        element = [number, (line, column)]
        self.tokens.append(element)

    # Função para adicionar variaveis e constantes
    def add_token(self, character, index, line, column):
        try:
            number = int(character)
            element = [Symbol.INTEGER.value, index, (line, column)]
            self.tokens.append(element)
        except:
            element = [Symbol.VARIABLE.value, index, (line, column)]
            self.tokens.append(element)

    # responsável por adicionar na tabela de símbolos
    def add_symbol_table(self, symbol, lexeme, line, column):
        global number

        if lexeme not in self.symbol_table:
            self.symbol_table.append(lexeme)
            number += 1

        self.add_token(lexeme, self.symbol_table.index(
            lexeme), line, column)

    def get_symbol_table(self):
        return self.symbol_table

    def get_tokens(self):
        return self.tokens

    def next(self):
        if self.source is not None:
            try:
                character = self.source.read(1)

                if character == '\r':
                    character = self.source.read(1)

                if character:
                    self.column += 1
                    return character
                else:
                    self.source.close()
                    self.source = None
                    return None
            except IOError as exception:
                print(exception)

        return None

    
    def parse(self, source):
        self.source = source
        self.tokens = []
        self.line = 1
        self.lexeme = None
        numeros = []  # Lista global para armazenar os números

        for line_number, line in enumerate(source.readlines(), start=1):
            words = line.split()

            if words:
                if re.search(r'^-?[0-9]\d*(\.\d+)?$', words[0]):
                    numeros.append(int(words[0]))

            self.verifica_ordem_numeros(words, line_number)


            if re.match(r'^\d+\s+rem', line.strip()):
                continue

            for word in words:
                #print(words)
                self.column = words.index(word) + 1
                self.q0(word)

            self.q3()
            self.line += 1
        self.SyntaxAnalysis()

        return self.error



    def q0(self, character):
        keywords = ('rem', 'if', 'input', 'let', 'print', 'goto', 'end', 'REM', 'IF', 'INPUT', 'LET', 'PRINT', 'GOTO', 'END')
        operadores = ('+', '-', '*', '/', '%', '=', '<', '>', '!', '<=', '>=' , '==', '!=')
        alfabeto = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

            # Verificar se a linha começa com "rem" e ignorar completamente
        if character.lower() == 'rem':
            return
        
        if re.search(r'^-?[0-9]\d*(\.\d+)?$', character):
            self.add_symbol_table(
                Symbol.INTEGER, character, self.line, self.column)
        elif character in keywords:
            self.q1(character, self.line, self.column)
        elif character in alfabeto:
            self.add_symbol_table(
                Symbol.VARIABLE, character, self.line, self.column)
        elif character in operadores:
            self.q2(character, self.line, self.column)
        elif character == 'rem':
            self.q1(character, self.line, self.column)
            pass
        else:
            self.lexeme = Token(character, Symbol.ERROR,
                                self.line, self.column)
            self.q99(character)


    # identificar palavras reservadas para a tabela de TOKENS
    def q1(self, character, line, column):
        match character.lower():
            case 'if':
                self.token_add(Symbol.IF.value, character, line, column)
            case 'rem':
                self.token_add(Symbol.REM.value, character, line, column)
            case 'let':
                self.token_add(Symbol.LET.value, character, line, column)
            case 'input':
                self.token_add(Symbol.INPUT.value, character, line, column)
            case 'print':
                self.token_add(Symbol.PRINT.value, character, line, column)
            case 'goto':
                self.token_add(Symbol.GOTO.value, character, line, column)
            case 'end':
                self.token_add(Symbol.END.value, character, line, column)
            case _:
                self.q99()
                print('Erro')
    
    # identificar operadores reservados para a tabela de TOKENS      
    def q2(self, character, line, column):
        match character:
            case '+':
                self.token_add(Symbol.ADD.value, character, line, column)
            case '-':
                self.token_add(Symbol.SUBTRACT.value, character, line, column)
            case '*':
                self.token_add(Symbol.MULTIPLY.value, character, line, column)
            case '/':
                self.token_add(Symbol.DIVIDE.value, character, line, column)
            case '%':
                self.token_add(Symbol.MODULO.value, character, line, column)
            case '=':
                self.token_add(Symbol.ASSIGNMENT.value, character, line, column)
            case '<':
                self.token_add(Symbol.LT.value, character, line, column)
            case '>':
                self.token_add(Symbol.GT.value, character, line, column)
            case '>=':
                self.token_add(Symbol.GE.value, character, line, column)
            case '<=':
                self.token_add(Symbol.LE.value, character, line, column)
            case '!=':
                self.token_add(Symbol.NE.value, character, line, column)
            case '==':
                self.token_add(Symbol.EQ.value, character, line, column)
            case _:
                self.q99()
                print('Erro')
                
    # Estado dedicado para criar o caracter de nova linha.
    def q3(self):
        element = [Symbol.LF.value, (self.line, self.column)]
        self.tokens.append(element)


    def q99(self, string):
        self.error = True
        error_message = f"Erro léxico na linha {self.lexeme.line}, coluna {self.lexeme.column}: Caractere não reconhecido: '{string}'"
        print(error_message)
        

        
    def verifica_ordem_numeros(self, words, line_number):
        global number
        try: 
            first_line = int(words[0])
            if first_line > number:
                number = first_line
            else:
                print(f"\nErro semântico: O Label não está em ordem crescente na linha {line_number}")
        except ValueError:
            print(f"\nErro semântico: Só pode haver números no Label, linha {line_number}")


    def SyntaxAnalysis(self):
        order = []
        for element in self.tokens:
            if element[0] != 10:
                order.append(element[0])

            else:
                # print(order)
                #print(order[0])
                self.syntax(order)
                order.clear()

    def syntax(self, order):
        match order[1]:
            case 61:
                pass
            case 62:
                self.case_input(order)
            case 63:
                self.case_let(order)
            case 64:
                self.case_print(order)
            case 65:
                self.case_goto(order)
            case 66:
                self.case_if(order, self.line, self.column)
            case 67:
                self.case_end(order)
            case _: 
                print(f'\nHá um erro sintático, existe uma linha que não tem palavras reservadas')

    def case_input(self, order):
        match order[2:]:
            case [41]:
                pass
            case _:
                print(f'\nErro sintático: no seu input')
                
    def case_end(self, order):
        match order[2:]:
            case [( 3 | 10 |  11 | 21 |  22 | 23 |  24 | 25 | 31 | 32 |  33 | 34 |  35 | 36 |  41 | 51 | 61 | 62 | 63 | 64 | 65 | 66 | 67 | 99)]:
                print(f'\nErro sintático: no seu end')
            case _:
                pass
    
    def case_print(self, order):
        match order[2:]:
            case[41]:
                pass
            case _:
                print(f'\nErro sintático: no seu print')
                
                
    def case_goto(self, order):
        match order[2:]:
            case [51]:
                pass
            case _:
                print(f'\nErro sintático: no seu goto')
                
    def case_let(self, order):
        match order[2:]:
            case [41, 11, (41 | 51)]:
                pass
            case [41, 11, 41, (21 | 22 | 23 | 24 | 25), (41 | 51)]:
                pass
            case _:
                print(f'\nErro sintático: no seu let')

           
            
    def case_if(self, order, line, column):
        match order[2:]:
            case [(41 | 51), (31 | 32 | 33 | 34 | 35 | 36 ), (41 | 51), 65, 51]:
                pass
            case _: 
                print(f'\nErro sintático: no seu if')
                
                



