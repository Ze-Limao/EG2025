from lark import Tree

def get_results_summary(varDec, varNotDec, varReDec):
    declaradas = []
    nao_declaradas = []
    re_declaradas = []

    for func, vars in varDec.items():
        for var, props in vars.items():
            declaradas.append({
                "função": func,
                "variável": var,
                "tipo": props.get("tipo"),
                "ocorrências": props.get("ocorr"),
                "re_declarada": props.get("redec", False)
            })

    for func, var in varNotDec:
        nao_declaradas.append({
            "função": func,
            "variável": var,
            "tipo": "❓ não declarada",
            "ocorrências": "-",
            "re_declarada": False
        })

    for func, entries in varReDec.items():
        for entry in entries:
            for var, props in entry.items():
                re_declaradas.append({
                    "função": func,
                    "variável": var,
                    "tipo": props.get("tipo"),
                    "ocorrências": props.get("ocorr"),
                    "re_declarada": True
                })

    return declaradas, nao_declaradas, re_declaradas


def get_warnings_and_errors(varDec, varNotDec, varReDec):
    outputWarnings = ["⚠️ Warnings:"]
    
    for func, vars in varDec.items():
        for var, props in vars.items():
            ocorr = props.get("ocorr")
            redec = props.get("redec", False)

            if ocorr == 0:
                outputWarnings.append(f"  - [Unused] A última declaração de '{var}' em '{func}' nunca foi usada (ocorr=0) → pode ser apagada.")
            if redec:
                outputWarnings.append(f"  - [Redeclared] '{var}' em '{func}' foi redeclarada.")

    for func, entries in varReDec.items():
        for entry in entries:
            for var, props in entry.items():
                if props.get("ocorr") == 0:
                    outputWarnings.append(f"  - [Redeclared & Unused] '{var}' em '{func}' foi redeclarada, mas a anterior nunca foi usada → pode ser apagada.")

        outputErros =["\n❌ Erros:"]
    if varNotDec:
        for var in varNotDec:
            outputErros.append(f"  - [Not Declared] '{var[1]}' foi usada em '{var[0]}' mas nunca foi declarada.")
    else:
        outputErros.append("  Nenhuma variável usada sem declaração.")

    return outputWarnings, outputErros


def get_type_summary(varDec):
    tipo_count = {}

    for func_vars in varDec.values():
        for var_props in func_vars.values():
            tipo = var_props.get("tipo")
            if tipo not in tipo_count:
                tipo_count[tipo] = 0
            tipo_count[tipo] += 1

    return tipo_count  # dicionário


def get_instruction_summary(results):
    return [f"{tipo}: {total}" for tipo, total in results.items()]


def get_nested_summary(results):
    return [f"{results}"]


def get_possible_fused_ifs(results):
    linhas = []
    if results:
        for i, tree in enumerate(results, 1):
            linhas.append(f"\n{i}. 🌿 Possível if aninhado fundível encontrado:")
            if isinstance(tree.children[0], Tree) and tree.children[0].data == "bool_expr":
                condicao_exterior = tree.children[0]
                linhas.append("     📌 Condição exterior:")
                linhas.append("      ➤ " + _format_bool_expr(condicao_exterior))

            try:
                cond_interna = tree.children[1].children[0].children[0].children[0]
                if isinstance(cond_interna, Tree) and cond_interna.data == "bool_expr":
                    linhas.append("     📌 Condição interior:")
                    linhas.append("      ➤ " + _format_bool_expr(cond_interna))
            except Exception as e:
                linhas.append("     ⚠️ Erro ao extrair condição interior: " + str(e))
    else:
        linhas.append("  Nenhum caso identificado.")
    return linhas


def _format_bool_expr(tree):
    """Tenta extrair uma expressão lógica legível de um bool_expr"""
    try:
        left = _extract_expr_value(tree.children[0])
        op = tree.children[1]
        right = _extract_expr_value(tree.children[2])
        return f"{left} {op} {right}"
    except:
        return "<expressão lógica complexa>"

def _extract_expr_value(expr_tree):
    """Extrai o valor de uma expressão simples (VAR, NUMBER, STRING...)"""
    if isinstance(expr_tree, Tree) and len(expr_tree.children) == 1:
        return str(expr_tree.children[0])
    return str(expr_tree)