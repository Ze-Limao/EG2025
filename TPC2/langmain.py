from lark import Lark

langrammar = """
start: function_def* "task" "main" "()" "-" ">" TYPE "{" command* return_command "}"

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

code = """
task add(int a, int b) -> int {
    return a + b;
}

task main() -> int {
    let int i = 0;
    loop (i <= 5) {
        show(i);
        i++;
    }
    
    for (let int j = 0; j < 3; j++) {
        check(i == j) {
            break;    
        }
        show(j);
    }
    
    let int result = add(3, 4);
    show(result);
    
    let int x = 10;
    check (x < 5) {
        show("x is less than 5");
    } also (x == 10) {
        show("x is 10");
    } otherwise {
        show("x is greater than 5 and not 10");
    }
    
    match (x) {
        option 5:
            show("x is 5");
        option 10:
            show("x is 10");
        standard:
            show("x is neither 5 nor 10");
    }
    
    return 0;
}
"""
def main():

    print("Hello, World!")

    #with open("langrammar.lark") as f:
    #    langrammar = f.read()

    parser = Lark(langrammar, start='start', parser='lalr')

    tree = parser.parse(code)

    print(tree.pretty())

if __name__ == "__main__":
    main()