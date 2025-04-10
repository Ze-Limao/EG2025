# TP 2

## OBJETIVOS PRINCIPAIS A IMPLEMENTAR

1. Lista de todas as vari´aveis do programa indicando os casos de: redeclara¸c˜ao ou n˜ao-declara¸c˜ao; vari´aveis
   usadas mas n˜ao inicializadas; vari´aveis declaradas e nunca mencionadas.
2. Total de var´aveis declaradas por cada Tipo de dados usados.
3. Total de instru¸c˜oes que formam o corpo do programa, indicando o n´umero de instru¸c˜oes de cada tipo (atribui¸c˜oes,
   leitura e escrita, condicionais e c´ıclicas).
4. Total de situa¸c˜oes em que estruturas de controlo surgem aninhadas em outras estruturas de controlo do mesmo
   ou de tipos diferentes.
5. Lista de situa¸c˜oes em que existam ifs aninhados que possam ser substitu´ıdos por um s´o if

## IMPLEMENTADOS

1. Lista de todas as vari´aveis do programa indicando os casos de: redeclara¸c˜ao ou n˜ao-declara¸c˜ao; vari´aveis
   usadas mas n˜ao inicializadas; vari´aveis declaradas e nunca mencionadas.
2. Total de var´aveis declaradas por cada Tipo de dados usados.
3. Total de instru¸c˜oes que formam o corpo do programa, indicando o n´umero de instru¸c˜oes de cada tipo (atribui¸c˜oes,
   leitura e escrita, condicionais e c´ıclicas).
4. Total de situa¸c˜oes em que estruturas de controlo surgem aninhadas em outras estruturas de controlo do mesmo
   ou de tipos diferentes.
5. Lista de situa¸c˜oes em que existam ifs aninhados que possam ser substitu´ıdos por um s´o if

## o que eu quero

varDec = {"funcName":{"nomeVar":{tipo:"", ocorr:N},
"nomeVar":{tipo:"", ocorr:N},
},
"funcName":{"nomeVar":{tipo:"", ocorr:N},
"nomeVar":{tipo:"", ocorr:N},
},
}
varNotDec = []
varReDec = {"funcName":{"nomeVar":{tipo:"", ocorr:N},
"nomeVar":{tipo:"", ocorr:N},
},}

as variaveis das funções
-> Função, nome, tipo, numero de ocorrencias
-> lista de declaradas
-> se n estiver na lista de declaradas quando usada adicionar à lista de não declaradas: nome,

## skill issues

1. não está a conseguir ler a gramatica de um ficheiro

## estrutura de ficheiros

- executador.py tem a main

- input é um ficheiro
