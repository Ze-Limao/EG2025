from lark.visitors import Interpreter
from lark import Tree

class InterpreterCondicoesECiclos(Interpreter):
    def __init__(self):
        self.counts = {
            "atribuicoes": 0,
            "escrita": 0,
            "condicionais": 0,
            "ciclos": 0
        }
        self.aninhamentos = 0
        self.if_fundidos = []  # lista de tuplos com nós ou info dos ifs fundíveis
        self.control_stack = []  # stack de estruturas de controlo para cenas aninhadas

    def start(self, tree):
        self.visit_children(tree)

    def function_def(self, tree):
        self.visit_children(tree)

    def return_command(self, tree):
        self.visit_children(tree)

    def command(self, tree):
        self.visit_children(tree)

    def parametros(self, tree):
        self.visit_children(tree)

    def param(self, tree):
        self.visit_children(tree)

    def function_call(self, tree):
        self.visit_children(tree)

    def expr(self, tree):
        self.visit_children(tree)

    def allocation(self, tree):
        self.counts["atribuicoes"] += 1

    def allocation_aux(self, tree):
        self.counts["atribuicoes"] += 1

    def variable_declaration(self, tree):
        self.counts["atribuicoes"] += 1

    def print_command(self, tree):
        self.counts["escrita"] += 1

    def option_command(self, tree):
        self.counts["condicionais"] += 1
    def standard_command(self,tree):
        self.counts["condicionais"] += 1

    def print_command(self, tree):
        self.counts["escrita"] += 1

    def check_command(self, tree):
        if self.control_stack:
            self.aninhamentos += 1
    
        self.counts["condicionais"] += 1
        self.control_stack.append("check")
    
        subchecks = 0
        other_commands = 0
    
        for child in tree.children:
            if isinstance(child, Tree) and child.data == "command" and len(child.children) > 0:
                grandchild = child.children[0]
        
                # Verifica se é conditional com exatamente 1 filho e esse filho é check_command
                if (
                    isinstance(grandchild, Tree)
                    and grandchild.data == "conditional"
                    and len(grandchild.children) == 1
                    and isinstance(grandchild.children[0], Tree)
                    and grandchild.children[0].data == "check_command"
                    and not any(
                        isinstance(child, Tree) and child.data in {"also_command", "otherwise_command"}
                        for child in tree.children)
                ):
                    subchecks += 1
                else:
                    other_commands += 1

    
        if subchecks == 1 and other_commands == 0:
            self.if_fundidos.append(tree)
    
        self.visit_children(tree)
        self.control_stack.pop()
    


    def also_command(self, tree):
        self.counts["condicionais"] += 1
        self.visit_children(tree)

    def otherwise_command(self, tree):
        self.counts["condicionais"] += 1
        self.visit_children(tree)

    def match_command(self, tree):
        if self.control_stack:
            self.aninhamentos += 1
        self.counts["condicionais"] += 1
        self.control_stack.append("match")
        self.visit_children(tree)
        self.control_stack.pop()

    def loop_loop(self, tree):
        if self.control_stack:
            self.aninhamentos += 1
        self.counts["ciclos"] += 1
        self.control_stack.append("loop")
        self.visit_children(tree)
        self.control_stack.pop()

    def foreach_loop(self, tree):
        if self.control_stack:
            self.aninhamentos += 1
        self.counts["ciclos"] += 1
        self.control_stack.append("foreach")
        self.visit_children(tree)
        self.control_stack.pop()

    def for_loop(self, tree):
        if self.control_stack:
            self.aninhamentos += 1
        self.counts["ciclos"] += 1
        self.control_stack.append("for")
        self.visit_children(tree)
        self.control_stack.pop()

    def summarize(self):
        return self.counts, self.aninhamentos, self.if_fundidos