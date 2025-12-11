*O código serve para realizar cadastro de alunos onde ficará armazenado em um mini banco de dados*

*Para executar o código corretamente, será necesário importar a biblioteca pandas e a os. Também será necessário  ter instalado o java, python e o pandas em sua máquina para não ocorrer erros na execução*


*Explicação das linhas de código*

Importação de Bibliotecas

import pandas as pd
import os


import pandas as pd
Carrega a biblioteca **Pandas**, muito utilizada para manipulação de tabelas e arquivos CSV.
O alias **pd** é usado como abreviação para facilitar a escrita do código.

import os
Importa o módulo os, que permite interação com o sistema operacional (não é muito usado neste código, mas pode auxiliar em verificações de arquivos).



Declaração de Constantes**


ARQUIVO_CSV = 'alunos.csv'
COLUNAS = ['Matricula', 'Nome', 'Rua', 'Numero', 'Bairro', 'Cidade', 'UF', 'Telefone', 'Email']


ARQUIVO_CSV: nome do arquivo onde os dados serão armazenados.
COLUNAS: lista com os nomes das colunas da tabela dos alunos.

Essas constantes evitam repetição e facilitam manutenção.



Função inicializar_dataframe()


def inicializar_dataframe():


Essa função é responsável por carregar o banco de dados (CSV) ou criar um novo caso ele ainda não exista.

Trecho principal:


try:
    df = pd.read_csv(ARQUIVO_CSV)
    df['Matricula'] = df['Matricula'].astype(int)


Tenta carregar o arquivo CSV para dentro de um **DataFrame**.
Converte a coluna “Matrícula” para inteiro.

Tratamento de erros:

Se o arquivo não existir:


except FileNotFoundError:
    df = pd.DataFrame(columns=COLUNAS)


Cria um DataFrame vazio com as colunas definidas.

Se o arquivo existir mas estiver vazio:


except pd.errors.EmptyDataError:


Cria DataFrame vazio e informa ao usuário.

Qualquer outro erro:


except Exception as e:


Retorna um DataFrame vazio e mostra o erro.



Função salvar_dataframe(df)

df.to_csv(ARQUIVO_CSV, index=False)


Essa função salva o DataFrame no arquivo CSV.

index=False significa que o índice do DataFrame não será salvo no arquivo.

Retorna:

True se der certo
False se ocorrer erro



Função gerar_matricula(df)

if df.empty:
    return 1
else:
    return df['Matricula'].max() + 1


Se o DataFrame estiver vazio → matrícula começa em 1.
Caso contrário → gera uma matrícula sequencial automática.



Função buscar_aluno(df, termo_busca)**

Responsável por localizar um aluno pelo nome OU matrícula.

Caso o usuário digite um número:

matricula = int(termo_busca)


Procura pela matrícula.

Caso o termo seja um texto:


resultado = df[df['Nome'].str.lower() == nome.lower()]


Procura pelo nome ignorando maiúsculas e minúsculas.

Retorna:

índice do aluno encontrado
dicionário com os dados
ou (None, None) se não achar



Função exibir_dados_aluno(dados)


for chave, valor in dados.items():


Exibe os dados do aluno na tela de forma organizada.



Função inserir_aluno(df)

Fluxo:

1. Gera uma matrícula automaticamente.
2. Solicita ao usuário os dados do aluno.
3. Cria um novo DataFrame com o aluno.
4. Junta os dados ao DataFrame principal.
5. Salva no CSV.
6. Retorna o DataFrame atualizado.

Cada campo é solicitado até que o usuário digite algo válido:


while True:
    valor = input(...)
    if valor:
        break



Função pesquisar_e_gerenciar_aluno(df)

Permite buscar um aluno e depois decidir:

 **Editar**
 **Remover**
 **Voltar ao menu**

Usa as funções:

* buscar_aluno()
* editar_aluno()
* remover_aluno()
* exibir_dados_aluno()



Função editar_aluno(df...)

1. Mostra quais campos podem ser editados.
2. Usuário escolhe o campo.
3. Digita o novo valor.
4. O DataFrame é atualizado.
5. O arquivo CSV é salvo.

Atualização ocorre assim:


df.loc[index_iloc, campo_a_editar] = novo_valor




Função remover_aluno(df...)

Pede confirmação:


if confirmacao == 'S':


Se confirmado:

Remove a linha do DataFrame:


df.drop(index=index_iloc)


Reorganiza os índices:


.reset_index(drop=True)


* Salva arquivo.


Função menu_principal()

Controla todo o programa.

Exibe o menu:

[1] INSERIR NOVO ALUNO
[2] PESQUISAR/EDITAR/REMOVER
[3] SAIR
```

Com base na escolha, chama a função adequada.



Execução do programa


if __name__ == "__main__":
    menu_principal()


Esse bloco garante que o menu só será executado se o arquivo for rodado diretamente, e não importado por outro programa.



