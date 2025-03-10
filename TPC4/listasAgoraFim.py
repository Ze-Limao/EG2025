from lark import Lark, Transformer, v_args

class intervalTransformerAcceptence(Transformer):
    '''
    Atributes:
        sentido (int): Represents the current direction of the signal (+1 or -1).
        anterior (float): Stores the endpoint of the previous interval.
        erro (bool): Flag indicating whether a constraint violation occurred.
    '''
    def __init__(self):
        self.started = 0
        self.podeAcabar = []
        self.erro = False

    @v_args(inline=True)
    def valor(self, valor):
        if valor == "agora":
            self.started +=1
            self.podeAcabar.append(False)
        elif valor == "fim":
            if self.started == 0:
                print(f"Error: Constraint CC1 violated. agora should appead before the fim).")
                self.erro = True
                return None  # Skip invalid interval
            if not self.podeAcabar[-1]:
                print(f"Error: Constraint CC1 violated. should appear a number between agora and fim).")
                self.erro = True
                return None  # Skip invalid interval
            self.started -=1
            self.podeAcabar.pop()
        else:
            if self.started != 0:
                self.podeAcabar[-1] = True

        return {"ok"}

    @v_args(inline=True)
    def valores(self, *valores):
        return [valor for valor in valores if valor is not None]

    @v_args(inline=True)
    def sentence(self, a,valores):
        return {"valores": valores}

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
    #tree = parser.parse("LISTA aaa .")
    #print(tree.pretty())
    
    #tree = parser.parse("LISTA 1 .")
    #print(tree.pretty())

    tree = parser.parse("Lista 1, 2, agora, 3, 4, fim, 7, 8.")
    print(tree.pretty())

    try:
        transformer = intervalTransformerAcceptence()
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
