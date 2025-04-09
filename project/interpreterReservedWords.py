from lark import Token
from lark.visitors import Interpreter


class InterpreterReservedWords(Interpreter):
    def __init__(self):
        self.current_func = "main"  # começa no main por padrão
        self.varDec = {}
        self.varReDec = {}
        self.varNotDec = []
        self._current_scope_vars = {}  # dicionário auxiliar para variáveis da função atual

    def start(self, tree):
        # "task main" está no final da regra start, então a visit das functions vem antes
        for child in tree.children:
            self.visit(child)

        # no final, adiciona o escopo de main
        if self.current_func == "main":
            self.varDec["main"] = self._current_scope_vars

    def function_def(self, tree):
        func_name_token = tree.children[0]
        func_name = func_name_token.value
        self.current_func = func_name
        self._current_scope_vars = {} #garante que está vazio

        # visita comandos dentro da função
        self.visit_children(tree)

        # salva no varDec
        self.varDec[func_name] = self._current_scope_vars
        self._current_scope_vars = {} #esvazia para o proximo
        self.current_func = "main"


    def variable_declaration(self, tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        # salva tipo e inicia ocorrências
        if var not in self._current_scope_vars.keys():
            self._current_scope_vars[var] = {"tipo": tipo, "ocorr": 0, "redec":False}
        else:
            if self.current_func not in self.varReDec.keys():
                self.varReDec[self.current_func] = [{var:self._current_scope_vars[var]}]
                self._current_scope_vars[var] = {"tipo": tipo, "ocorr": 0, "redec":True}
            else:
                self.varReDec[self.current_func] += [{var:self._current_scope_vars[var]}]
                self._current_scope_vars[var] = {"tipo": tipo, "ocorr": 0, "redec":True}



        self.visit(tree.children[2])  # expr

    def param(self, tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        self._current_scope_vars[var] = {"tipo": tipo, "ocorr": 0, "redec":False}

    def allocation(self, tree):
        var_token = tree.children[0]
        if isinstance(var_token, Token) and var_token.type == "VAR":
            self._register_var_usage(var_token.value)
        self.visit_children(tree)

    def allocation_aux(self, tree):
        var_token = tree.children[0]
        if isinstance(var_token, Token) and var_token.type == "VAR":
            self._register_var_usage(var_token.value)
        self.visit_children(tree)

    def print_command(self, tree):
        var_token = tree.children[0]
        if isinstance(var_token, Token) and var_token.type == "VAR":
            self._register_var_usage(var_token.value)
        self.visit_children(tree)

    def expr(self, tree):
        for child in tree.children:
            if isinstance(child, Token) and child.type == "VAR":
                self._register_var_usage(child.value)
        self.visit_children(tree)

    def function_call(self, tree):
        self.visit_children(tree)

    def _register_var_usage(self, var_name):
        if var_name in self._current_scope_vars:
            self._current_scope_vars[var_name]["ocorr"] += 1
        else:
            self.varNotDec.append([self.current_func,var_name])

    def get_results(self):
        return self.varDec, self.varNotDec, self.varReDec
