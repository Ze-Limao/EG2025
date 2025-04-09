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

    print("\n♻️ Variáveis Re-declaradas (varReDec):")
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

    print("\n Total de Variáveis por Tipo de Dados:")
    for tipo, count in tipo_count.items():
        print(f"  - {tipo}: {count}")