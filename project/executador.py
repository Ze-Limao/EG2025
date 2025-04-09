from lark import Lark
from interpreterReservedWords import InterpreterReservedWords
from printDeCenas import print_results, print_warnings_and_errors, print_type_summary

langrammar = """
start: function_def* "task" "main" "()" "-" ">" ret_type "{" command* return_command "}"

ret_type: TYPE      -> return_type

command: variable_declaration ";"
    | allocation ";"
    | print_command ";"
    | function_call ";"
    | loop
    | conditional
    | "break" ";"
    | "continue" ";"

variable_declaration: "let" TYPE VAR "=" expr

allocation_aux: VAR ASS_OP expr
        | VAR "++"
        | VAR "--"
                    
allocation: VAR "=" expr
        | allocation_aux
        
expr: VAR
    | NUMBER
    | STRING
    | function_call
    | expr OP expr
    | expr LOGICAL_OP expr
    
print_command: "show" "(" VAR ")"
        | "show" "(" NUMBER ")"
        | "show" "(" STRING ")"
        
function_def: "task" VAR "(" parametros? ")" "-" ">" TYPE "{" command* return_command "}"

return_command: "return" expr ";"

parametros: param "," parametros
    | param

param: TYPE VAR

function_call: VAR "(" arg_list? ")"

arg_list: expr "," arg_list
    | expr

loop: for_loop | loop_loop

for_loop: "for" "(" variable_declaration ";" for_cond ";" for_update ")" "{" command* "}" 

for_cond: bool_expr

for_update: allocation_aux

loop_loop: "loop" "(" bool_expr ")" "{" command* "}"

conditional: check_command | match_command

check_command: "check" "(" bool_expr ")" "{" command* "}" (also_command)* (otherwise_command)?

also_command: "also" "(" bool_expr ")" "{" command* "}"

otherwise_command: "otherwise" "{" command* "}"

match_command: "match" "(" expr ")" "{" option_command* standard_command? "}"

option_command: "option" expr ":" command*

standard_command: "standard" ":" command*

bool_expr: expr LOGICAL_OP expr
    | function_call

TYPE: "int" | "double" | "tuple" | "string" | "array" | "bool" | "void"

VAR: /[a-z]+(_[a-z]+)*/

NUMBER: /-?\\d+(\\.\\d+)?/

STRING: /".*"/

OP: "+" | "-" | "*" | "/"

LOGICAL_OP: "==" | "!=" | "<=" | ">=" | "<" | ">"

ASS_OP: "+=" | "-=" | "*=" | "/="

%import common.WS
%ignore WS
"""


def main():
    # Load the grammar from the file
    #with open("grammar.lark") as f:
    #    grammar = f.read()

    parser = Lark(langrammar, parser="lalr")

    with open("input.txt") as f:
        prog = f.read()
    
    tree = parser.parse(prog)
    #print(tree.pretty())

    analyzer = InterpreterReservedWords()
    analyzer.visit(tree)
    varDec, varNotDec,varReDec = analyzer.get_results()

    
    while True:
        print("\n📋 MENU:")
        print("1. Mostrar variáveis (declaradas, não declaradas e re-declaradas)")
        print("2. Mostrar warnings e erros")
        print("3. Mostrar total de variáveis por tipo de dados")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print_results(varDec, varNotDec, varReDec)
        elif opcao == "2":
            print_warnings_and_errors(varDec, varNotDec, varReDec)
        elif opcao == "3":
            print_type_summary(varDec)
        elif opcao == "0":
            print("👋 Saindo...")
            break
        
        else:
            print("❗ Opção inválida. Tente novamente.")


main()