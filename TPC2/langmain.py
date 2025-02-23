from lark import Lark

langrammar = """
start: function_declaration* "task" "main" "()" "-" ">" TYPE "{" statement* return_statement "}"

statement: variable_declaration ";"
    | assignment ";"
    | print_statement ";"
    | function_call ";"
    | loop
    | conditional
    | "break" ";"
    | "continue" ";"

variable_declaration: "let" TYPE VAR "=" expr

assignment_aux: VAR ASS_OP expr
        | VAR "++"
        | VAR "--"
                    
assignment: VAR "=" expr
        | assignment_aux
        
expr: VAR
    | NUMBER
    | STRING
    | function_call
    | expr OP expr
    | expr LOGICAL_OP expr
    
print_statement: "show" "(" VAR ")"
        | "show" "(" NUMBER ")"
        | "show" "(" STRING ")"
        
function_declaration: "task" VAR "(" param_list? ")" "-" ">" TYPE "{" statement* return_statement "}"

return_statement: "return" expr ";"

param_list: param "," param_list
    | param

param: TYPE VAR

function_call: VAR "(" arg_list? ")"

arg_list: expr "," arg_list
    | expr

loop: for_loop | while_loop

for_loop: "for" "(" variable_declaration ";" for_cond ";" for_update ")" "{" statement* "}" 

for_cond: bool_expr

for_update: assignment_aux

while_loop: "loop" "(" bool_expr ")" "{" statement* "}"

conditional: if_statement | switch_statement

if_statement: "check" "(" bool_expr ")" "{" statement* "}" (elif_statement)* (else_statement)?

elif_statement: "elif" "(" bool_expr ")" "{" statement* "}"

else_statement: "otherwise" "{" statement* "}"

switch_statement: "match" "(" expr ")" "{" case_statement* default_statement? "}"

case_statement: "option" expr ":" statement*

default_statement: "standard" ":" statement*

bool_expr: expr LOGICAL_OP expr
    | function_call

TYPE.2: "int" | "double" | "string" | "set" | "array" | "tuplo"
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
        show(j);
    }
    
    let int result = add(3, 4);
    show(result);
    
    let int x = 10;
    check (x < 5) {
        show("x is less than 5");
    } elif (x == 10) {
        show("x is 10");
    } otherwise {
        show("x is greater than 5 and not 10");
    }
    
    match (x) {
        option 5:
            show("x is 5");
            break;
        option 10:
            show("x is 10");
            break;
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