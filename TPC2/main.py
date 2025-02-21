from lark import Lark, Transformer, v_args

class intervalTransformer(Transformer):
    '''
    Atributes:
        sentido (int): Represents the current direction of the signal (+1 or -1).
        anterior (float): Stores the endpoint of the previous interval.
        erro (bool): Flag indicating whether a constraint violation occurred
    '''
    def __init__(self):
        self.sentido = 0
        self.anterior = float('-inf')
        self.erro = False

    @v_args(inline=True)
    def plus(self):
        self.sentido = 1
        print("Signal set to + (growing).")
        return 1
    
    @v_args(inline=True)
    def minus(self):
        self.sentido = -1
        print("Signal set to - (decreasing).")
        return -1

    @v_args(inline=True)
    def interval(self, left, right):
        left = int(left)
        right = int(right)
        if self.sentido == 1:
            if right <= left:
                print(f"Error: Constraint CC1 violated. right ({right}) must be greater than left ({left}).")
                self.erro = True
                return None  # Skip invalid interval
            if left < self.anterior:
                print(f"Error: Constraint CC2 violated. left ({left}) must be greater than or equal to the previous right ({self.anterior}).")
                self.erro = True
                return None  # Skip invalid interval
        elif self.sentido == -1:
            if right >= left:
                print(f"Error: Constraint CC1 violated. right ({right}) must be less than left ({left}).")
                self.erro = True
                return None  # Skip invalid interval
            if left > self.anterior:
                print(f"Error: Constraint CC2 violated. left ({left}) must be less than or equal to the previous right ({self.anterior}).")
                self.erro = True
                return None  # Skip invalid interval

        self.anterior = right
        return {"left": left, "right": right}
    
    @v_args(inline=True)
    def intervals(self, *intervals):
        return [interval for interval in intervals if interval is not None]

    @v_args(inline=True)
    def sentence(self, signal, intervals):
        return {"sentido": signal, "intervals": intervals}

    @v_args(inline=True)
    def start(self, sentence):
        return sentence

    def empty(self, _):
        return []

def main():
    # Load the grammar from the file
    with open("grammar.lark") as f:
        grammar = f.read()

    parser = Lark(grammar, parser="lalr")

    # print tree
    tree = parser.parse("+ [1:5] [10:20].")
    print(tree.pretty())

    try:
        transformer = intervalTransformer()
        result = transformer.transform(tree)
        if transformer.erro:
            print("\nParsing failed: One or more constraints were violated.")
        else:
            print("\nParsing successful: All constraints satisfied.")
            print("Parsed intervals:", result)
    except Exception as e:
        print(f"\nParsing error: {e}")

if __name__ == "__main__":
    main()
