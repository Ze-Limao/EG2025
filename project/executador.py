from lark import Lark
from interpreterReservedWords import InterpreterReservedWords
import webbrowser

from interpreterCondicoesECiclos import InterpreterCondicoesECiclos
from printDeCenas import print_results, print_warnings_and_errors, print_type_summary, print_analysis_results,print_total_aninhados,print_possiveis_Opt_ifs
from getDeCenas import get_results_summary, get_warnings_and_errors, get_type_summary, get_instruction_summary, get_nested_summary, get_possible_fused_ifs

from htmlcreator import gerar_relatorio_html


def menu(varDec, varNotDec, varReDec, counts, aninhamentos, if_fundidos):
    while True:
        print("\n📋 MENU:")
        print("1. Mostrar variáveis (declaradas, não declaradas e re-declaradas)")
        print("2. Mostrar warnings e erros")
        print("3. Mostrar total de variáveis por tipo de dados")
        print("4. Mostar total de instruções por tipo")
        print("5. Mostar total de estruturas de controlo aninhadas")
        print("6. Mostrar ifs aninhados que podem ser unidos")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print_results(varDec, varNotDec, varReDec)
        elif opcao == "2":
            print_warnings_and_errors(varDec, varNotDec, varReDec)
        elif opcao == "3":
            print_type_summary(varDec)
        elif opcao == "4":
            print_analysis_results(counts)
        elif opcao == "5":
            print_total_aninhados(aninhamentos)
        elif opcao == "6":
            print_possiveis_Opt_ifs(if_fundidos)
        elif opcao == "0":
            print("👋 Saindo...")
            break
        
        else:
            print("❗ Opção inválida. Tente novamente.")

def main():
    # Load the grammar from the file
    with open("grammar.lark") as f:
        grammar = f.read()

    parser = Lark(grammar, parser="lalr")

    with open("input2.txt") as f:
        prog = f.read()
    
    tree = parser.parse(prog)
    #print(tree.pretty())

    analyzer = InterpreterReservedWords()
    analyzer.visit(tree)
    analyzer2 = InterpreterCondicoesECiclos()
    analyzer2.visit(tree)
    varDec, varNotDec,varReDec = analyzer.get_results()

    counts, aninhamentos, if_fundidos = analyzer2.summarize()

    declaradas, nao_declaradas, re_declaradas = get_results_summary(varDec, varNotDec, varReDec)
    warnings, erros = get_warnings_and_errors(varDec, varNotDec, varReDec)
    resumo_tipos = get_type_summary(varDec)
    resumo_instr = get_instruction_summary(counts)
    resumo_aninhados = get_nested_summary(aninhamentos)
    ifs_fundidos = get_possible_fused_ifs(if_fundidos)
    # Depois usas isso como input no gerador de HTML que já te mostrei:
    gerar_relatorio_html(
    prog,
    declaradas, 
    nao_declaradas, 
    re_declaradas,
    warnings,
    erros,
    resumo_tipos,
    resumo_instr,
    resumo_aninhados,
    ifs_fundidos
    )

    webbrowser.open("relatorio_analise.html")
    #menu(varDec, varNotDec, varReDec, counts, aninhamentos, if_fundidos)    

main()