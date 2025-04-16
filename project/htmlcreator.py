from datetime import datetime
import os

def gerar_relatorio_html(
    prog,
    declaradas,
    nao_declaradas,
    re_declaradas,
    warnings,
    erros,
    resumo_tipos,
    resumo_instr,
    resumo_aninhados,
    ifs_fundidos,
    output_path="relatorio_analise.html"
):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def format_lista(lista):
        return "<br>".join(lista) if lista else "<i>(sem dados)</i>"

    def format_dict(dicionario):
        return "<br>".join([f"{k}: {v}" for k, v in dicionario.items()]) if dicionario else "<i>(sem dados)</i>"


    def format_tabela_variaveis(lista):
        if not lista:
            return "<i>(nenhuma variável encontrada)</i>"
        html = """
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #eef;">
                    <th>Função</th>
                    <th>Variável</th>
                    <th>Tipo</th>
                    <th>Ocorrências</th>
                    <th>Re-declarada</th>
                </tr>
            </thead>
            <tbody>
        """
        for item in lista:
            html += f"""
            <tr>
                <td>{item['função']}</td>
                <td>{item['variável']}</td>
                <td>{item['tipo']}</td>
                <td>{item['ocorrências']}</td>
                <td>{"✅" if item['re_declarada'] else "❌"}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
    
    
    def format_tabela_nao_declaradas(lista):
        if not lista:
            return "<i>(nenhuma variável não declarada)</i>"
        html = """
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #fdd;">
                    <th>Função</th>
                    <th>Variável</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
        """
        for item in lista:
            html += f"""
            <tr>
                <td>{item['função']}</td>
                <td>{item['variável']}</td>
                <td>❗Não declarada</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
    
    
    def format_tabela_redeclaradas(lista):
        if not lista:
            return "<i>(nenhuma variável re-declarada)</i>"
        html = """
        <table style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr style="background-color: #ffd;">
                    <th>Função</th>
                    <th>Variável</th>
                    <th>Tipo</th>
                    <th>Ocorrências</th>
                </tr>
            </thead>
            <tbody>
        """
        for item in lista:
            html += f"""
            <tr>
                <td>{item['função']}</td>
                <td>{item['variável']}</td>
                <td>{item['tipo']}</td>
                <td>{item['ocorrências']}</td>
            </tr>
            """
        html += "</tbody></table>"
        return html
    
    html = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <title>Relatório de Análise</title>
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background: #f9f9f9;
                margin: 40px;
                color: #333;
            }}
            h1, h2 {{
                margin-top : 0px;
                color: #2c3e50;
            }}
            section {{
                margin-bottom: 20px;
                padding: 20px;
                border-radius: 10px;
                background: #fff;
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            }}
            .timestamp {{
                font-size: 0.9em;
                color: #888;
                text-align: right;
            }}
            .mono {{
                font-family: monospace;
                white-space: pre-wrap;
            }}

            .titulo {{
                display: flex;
                cursor: pointer;
                user-select: none;
            }}

            .seta {{
                font-size: 24px;
                margin-right: 10px;
                transition: transform 0.3s ease;
            }}

            .seta.ativa {{
                transform: rotate(90deg);
            }}

            .bloco-codigo {{
                margin-top: 10px;
                display: none;
                background-color: #f5f5f5;
                border-radius: 6px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
                white-space: pre-wrap;
            }}

            .bloco-codigo.visivel {{
                padding: 10px;
                display: block;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
                font-size: 14px;
                background-color: #fff;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                border-radius: 10px;
                overflow: hidden;
            }}

            th, td {{
                text-align: left;
                padding: 12px 15px;
                border-bottom: 1px solid #eee;
            }}

            th {{
                background-color: #f3f4f6;
                font-weight: 600;
                color: #2c3e50;
            }}

            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            tr:hover {{
                background-color: #f1f5f9;
                transition: background 0.3s ease;
            }}
        </style>
    </head>
    <body>
        <div style="display: flex; justify-content: space-between;align-items: center;">
            <h1 style="margin-bottom: 0px">Relatório de Análise de Código</h1>
            <img src="logo.png" alt="Logo" style="height: 60px;">
        </div>

        <div class="timestamp">Gerado em: {now}</div>

        <section>
                <div id="cabecalho" class="titulo">
                    <div id="seta" class="seta">➡️</div>
                    <h2 style="margin-bottom: 0px"> Código</h2> 
                </div>
                <div id="blocoCodigo" class="bloco-codigo">
                    <code>
                    {prog}
                    </code>
                </div>
            <script>
                const seta = document.getElementById("seta");
                const bloco = document.getElementById("blocoCodigo");

                document.getElementById("cabecalho").addEventListener("click", () => {{
        
                    seta.classList.toggle("ativa");
                    bloco.classList.toggle("visivel");
                }});
  </script>
        </section>
        
        <section>
          <h2>📦 Variáveis Declaradas</h2>
          {format_tabela_variaveis(declaradas)}
        </section>

        <section>
          <h2>🚫 Variáveis Não Declaradas</h2>
          {format_tabela_nao_declaradas(nao_declaradas)}
        </section>

        <section>
          <h2>♻️ Variáveis Re-declaradas</h2>
          {format_tabela_redeclaradas(re_declaradas)}
        </section>


        <section>
            <h2> Warnings e Erros</h2>
            <div class="mono" style="color: #eead2d;")>{format_lista(warnings)}</div>
            <div class="mono" style="color: red;">{format_lista(erros)}</div>
        </section>


        <section>
            <h2> Total de Variáveis por Tipo de Dados</h2>
            <div class="mono">{format_dict(resumo_tipos)}</div>
        </section>

        <section>
            <h2> Total de Instruções por Tipo</h2>
            <div class="mono">{format_lista(resumo_instr)}</div>
        </section>

        <section>
            <h2> Estruturas de Controlo Aninhadas</h2>
            <div class="mono">{format_lista(resumo_aninhados)}</div>
        </section>

        <section>
            <h2> Ifs Aninhados que Podem Ser Fundidos</h2>
            <div class="mono">{format_lista(ifs_fundidos)}</div>
        </section>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Relatório gerado com sucesso: {os.path.abspath(output_path)}")
