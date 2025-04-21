from lark import Lark


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

    with open("langrammar.lark") as f:
        langrammar = f.read()

    parser = Lark(langrammar, start='start', parser='lalr')

    tree = parser.parse(code)

    print(tree.pretty())

if __name__ == "__main__":
    main()