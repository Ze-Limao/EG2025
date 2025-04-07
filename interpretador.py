from lark import Discard
from lark import Lark,Token,Tree
from lark.tree import pydot__tree_to_png
from lark.visitors import Interpreter

class MyInterpreter(Interpreter):
    def __init__(self):
        self.comprimento = 0
        self.soma = 0

    def start(self, tree):
        print("Entrei na Raiz, vou visitar os Elementos")
        a = 0
        alunosTotal = 0
        for t in tree.children:
            alunosTotal += self.visit(t)
            a+=1
        print("Elementos visitados, vou regressar à main()")
        return (a, alunosTotal)

    def turmas(self,tree):
       turma = self.visit(tree.children[0])
       alunos = self.visit(tree.children[1])
       print(f"turma{turma},é constituida por:{alunos}")
       return len(alunos)
    
    def turma(self,tree):
        r = self.visit_children(tree)
        if(r[0].type=='PALAVRA'):
          return str(r[0])
        else:
          return 
       

    def alunos(self,tree):
        r = self.visit_children(tree)
        r= []
        for aluno in tree.children:
          if (aluno.data == 'aluno' and type(aluno)==Tree):
            al = self.visit(aluno)
            r += [al[0]]
            print(f"o aluno {al[0]} tem média {al[1]}")
        return r

    def aluno(self,tree):#falta os valores
        r = tree.children[0]
        media = self.visit(tree.children[1])
        if(r.type=='PALAVRA'):
          return str(r),media
        else:
          return 

    def valores(self, tree):
        r=0
        i = 0
        for elemento in tree.children:
          i+=1
          if (elemento.data == 'valor' and type(elemento)==Tree):
            r += self.visit(elemento)
        return r/i

    def valor(self, tree):
        r = tree.children[0]
        if(r.type=='NUMERO'):
          self.comprimento += 1
          return int(r)
        else:
          return 0



input= """
TURMA A
ana (12, 13, 15, 12, 13, 15, 14);
joao (9,7,3,6,9);
xico (12,16).
TURMA B
Goncalo (12, 13, 15, 12, 13, 15, 14);
Ze (9,7,3,6,9,12);
Chino (12,16).
"""


def main():
    # Load the grammar from the file
    with open("grammar.lark") as f:
        grammar = f.read()

    parser = Lark(grammar, parser="lalr")


    tree = parser.parse(input)
    #print(tree.pretty())

    data = MyInterpreter().visit(tree)
    print("total de turmas ",data[0]," total de alunos: ",data[1])

main()