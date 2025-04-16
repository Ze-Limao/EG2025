from lark import Tree

def print_results(varDec, varNotDec, varReDec):
    print("\n📦 Variáveis Declaradas (varDec):")
    for func, vars in varDec.items():
        print(f"\n  Função: {func}")
        for var, props in vars.items():
            tipo = props.get("tipo")
            ocorr = props.get("ocorr")
            redec = props.get("redec", False)
            print(f"    - {var}: tipo={tipo}, ocorrências={ocorr}, redec={redec}")

    print("\n🚫 Variáveis Usadas mas Não Declaradas (varNotDec):")
    if varNotDec:
        for var in varNotDec:
            print(f"  - {var[1]} in {var[0]}")
    else:
        print("  (nenhuma)")

    print("\n♻️  Variáveis Re-declaradas (varReDec):")
    if varReDec:
        for func, entries in varReDec.items():
            print(f"\n  Função: {func}")
            for entry in entries:
                for var, props in entry.items():
                    tipo = props.get("tipo")
                    ocorr = props.get("ocorr")
                    print(f"    - {var}: tipo={tipo}, ocorrências={ocorr}")
    else:
        print("  (nenhuma)")

def print_warnings_and_errors(varDec, varNotDec, varReDec):
    print("\n⚠️  Warnings:")
    for func, vars in varDec.items():
        for var, props in vars.items():
            ocorr = props.get("ocorr")
            redec = props.get("redec", False)

            if ocorr == 0:
                print(f"\033[93m  - [Unused] A ultima declaração de '{var}' em '{func}' nunca foi usada (ocorr=0) → pode ser apagada.\033[0m")
            if redec:
                print(f"\033[93m  - [Redeclared] '{var}' em '{func}' foi redeclarada.\033[0m")

    for func, entries in varReDec.items():
        for entry in entries:
            for var, props in entry.items():
                if props.get("ocorr") == 0:
                    print(f"\033[93m  - [Redeclared & Unused] '{var}' em '{func}' foi redeclarada porém a declaração anterior nunca foi usada (ocorr=0) → pode ser apagada.\033[0m")

    print("\n❌ Erros:")
    if varNotDec:
        for var in varNotDec:
            print(f"\033[91m  - [Not Declared] '{var[1]}' foi usada em '{var[0]}' mas nunca declarada.\033[0m")
    else:
        print("  Nenhuma variável usada sem declaração.")



def print_type_summary(varDec):
    tipo_count = {}

    for func_vars in varDec.values():
        for var_props in func_vars.values():
            tipo = var_props.get("tipo")
            if tipo not in tipo_count:
                tipo_count[tipo] = 0
            tipo_count[tipo] += 1

    print("\n📋Total de Variáveis por Tipo de Dados:")
    for tipo, count in tipo_count.items():
        print(f"  - {tipo}: {count}")

def print_analysis_results(results):
    print("\n📊 Total de instruções por tipo:")
    for tipo, total in results.items():
        print(f"  - {tipo}: {total}")  # ifs: check|match|also|otherwise|option|standard

def print_total_aninhados(results):
    print(f"\n🪜  Total de estruturas de controlo aninhadas: {results}")

def print_possiveis_Opt_ifs(results):
    print("\n🗿 Ifs aninhados que podem ser fundidos:")
    if results:
        for i, tree in enumerate(results, 1):
            print(f"\n  {i}. 🌿 Possível if aninhado fundível encontrado:")
            
            # Mostramos a condição principal
            if isinstance(tree.children[0], Tree) and tree.children[0].data == "bool_expr":
                condicao_exterior = tree.children[0]
                print("     📌 Condição exterior:")
                print("      ➤", _format_bool_expr(condicao_exterior))
            
# Mostramos a condição interna
            try:
                cond_interna = tree.children[1].children[0].children[0].children[0]
                if isinstance(cond_interna, Tree) and cond_interna.data == "bool_expr":
                    print("     📌 Condição interior:")
                    print("      ➤", _format_bool_expr(cond_interna))
            except Exception as e:
                print("     ⚠️ Erro ao extrair condição interior:", e)
    else:
        print("  Nenhum caso identificado")

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