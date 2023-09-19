import sys
from Analyzer import LexicalAnalysis
from Symbol import Symbol
from Analyzer import LexicalAnalysis


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python .\Compiler.py arquivo_de_entrada")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        source = open(input_file, 'r')
    except IOError as exception:
        print(f"Erro ao abrir o arquivo: {exception}")
        sys.exit(1)
    
    lexer = LexicalAnalysis()
    error = lexer.parse(source)


    if not error:

        lexer.print_tokens_and_symbols()
    

    source.close()