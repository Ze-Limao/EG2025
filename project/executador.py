from lark import Lark
from interpreterReservedWords import InterpreterReservedWords
import webbrowser

from interpreterCondicoesECiclos import InterpreterCondicoesECiclos
from printDeCenas import print_results, print_warnings_and_errors, print_type_summary, print_analysis_results,print_total_aninhados,print_possiveis_Opt_ifs
from getDeCenas import get_results_summary, get_warnings_and_errors, get_type_summary, get_instruction_summary, get_nested_summary, get_possible_fused_ifs

from htmlcreator import gerar_relatorio_html
langrammar = """
start: function_def* main_func

main_func : "task" "main" "()" "-" ">" ret_type "{" command* return_command "}"

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


array_access: VAR "[" NUMBER "]"

allocation: VAR "=" expr
        | array_access "=" expr
        | allocation_aux
        
array_expr: "[" element_list? "]"

element_list: NUMBER ("," NUMBER)*


expr: VAR
    | NUMBER
    | STRING
    | function_call
    | expr OP expr
    | expr LOGICAL_OP expr
    | array_expr
    | array_access
    
print_command: "show" "(" VAR ")"
        | "show" "(" NUMBER ")"
        | "show" "(" STRING ")"
        | "show" "(" array_access ")"
        
function_def: "task" VAR "(" parametros? ")" "-" ">" TYPE "{" command* return_command "}"

return_command: "return" expr ";"

parametros: param "," parametros
    | param

param: TYPE VAR

function_call: VAR "(" arg_list? ")"

arg_list: expr "," arg_list
    | expr

foreach_loop: "foreach" "(" VAR "in" expr ")" "{" command* "}"

loop: for_loop | loop_loop | foreach_loop

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
def menu(varDec, varNotDec, varReDec, counts, aninhamentos, if_fundidos):
    while True:
        print("\n📋 MENU:")
        print("1. Mostrar variáveis (declaradas, não declaradas e re-declaradas)")
        print("2. Mostrar warnings e erros")
        print("3. Mostrar total de variáveis por tipo de dados")
        print("4. Mostar total de instruções por tipo")
        print("5. Mostar total de estruturas de controlo aninhadas")
        print("6. Mostrar ifs aninhados que podem ser unidos")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print_results(varDec, varNotDec, varReDec)
        elif opcao == "2":
            print_warnings_and_errors(varDec, varNotDec, varReDec)
        elif opcao == "3":
            print_type_summary(varDec)
        elif opcao == "4":
            print_analysis_results(counts)
        elif opcao == "5":
            print_total_aninhados(aninhamentos)
        elif opcao == "6":
            print_possiveis_Opt_ifs(if_fundidos)
        elif opcao == "0":
            print("👋 Saindo...")
            break
        
        else:
            print("❗ Opção inválida. Tente novamente.")

def main():
    # Load the grammar from the file
    #with open("grammar.lark") as f:
    #    grammar = f.read()

    parser = Lark(langrammar, parser="lalr")

    with open("input2.txt") as f:
        prog = f.read()
    
    tree = parser.parse(prog)
    #print(tree.pretty())

    analyzer = InterpreterReservedWords()
    analyzer.visit(tree)
    analyzer2 = InterpreterCondicoesECiclos()
    analyzer2.visit(tree)
    varDec, varNotDec,varReDec = analyzer.get_results()

    counts, aninhamentos, if_fundidos = analyzer2.summarize()

    resultados_gerais = get_results_summary(varDec, varNotDec, varReDec)
    warnings, erros = get_warnings_and_errors(varDec, varNotDec, varReDec)
    resumo_tipos = get_type_summary(varDec)
    resumo_instr = get_instruction_summary(counts)
    resumo_aninhados = get_nested_summary(aninhamentos)
    ifs_fundidos = get_possible_fused_ifs(if_fundidos)
    # Depois usas isso como input no gerador de HTML que já te mostrei:
    gerar_relatorio_html(
    prog,
    resultados_gerais,
    warnings,
    erros,
    resumo_tipos,
    resumo_instr,
    resumo_aninhados,
    ifs_fundidos
    )

    webbrowser.open("relatorio_analise.html")
    menu()    

main()