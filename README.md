--O código serve para realizar cadastro de alunos onde ficará armazenado em um mini banco de dados--

--Para executar o código corretamente, será necesário importar a biblioteca pandas e a os. Também será necessário  ter instalado o java, python e o pandas em sua máquina para não ocorrer erros na execução--


--Explicação das linhas de código--

--Importação de Bibliotecas--

import pandas as pd
import os


--import pandas as pd--
Carrega a biblioteca --Pandas--, muito utilizada para manipulação de tabelas e arquivos CSV.
O alias --pd-- é usado como abreviação para facilitar a escrita do código.

--import os--
Importa o módulo os, que permite interação com o sistema operacional (não é muito usado neste código, mas pode auxiliar em verificações de arquivos).



--Declaração de Constantes--


--ARQUIVO_CSV = 'alunos.csv'--
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



---Código sem explicação---

import pandas as pd
import os

ARQUIVO_CSV = 'alunos.csv'
COLUNAS = ['Matricula', 'Nome', 'Rua', 'Numero', 'Bairro', 'Cidade', 'UF', 'Telefone', 'Email']

def inicializar_dataframe():
    
    try:
        df = pd.read_csv(ARQUIVO_CSV)
        df['Matricula'] = df['Matricula'].astype(int)
    except FileNotFoundError:
        df = pd.DataFrame(columns=COLUNAS)
        print(f"Arquivo '{ARQUIVO_CSV}' não encontrado. Criando um novo sistema de cadastro.")
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=COLUNAS)
        print(f"Arquivo '{ARQUIVO_CSV}' está vazio. Iniciando um novo cadastro.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        df = pd.DataFrame(columns=COLUNAS) # Cria um DF vazio como fallback
    return df

def salvar_dataframe(df):
    try:
        df.to_csv(ARQUIVO_CSV, index=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
        return False

def gerar_matricula(df):
    if df.empty:
        return 1
    else:
        return df['Matricula'].max() + 1

def buscar_aluno(df, termo_busca):
    if df.empty:
        return None, None

    try:
        matricula = int(termo_busca)
        resultado = df[df['Matricula'] == matricula]
        if not resultado.empty:
            return resultado.index[0], resultado.iloc[0].to_dict()

    except ValueError:
        nome = str(termo_busca).strip()
        resultado = df[df['Nome'].str.lower() == nome.lower()]
        if not resultado.empty:
            return resultado.index[0], resultado.iloc[0].to_dict()

    return None, None

def exibir_dados_aluno(dados):
    print("\n--- DADOS DO ALUNO ENCONTRADO ---")
    for chave, valor in dados.items():
        print(f"**{chave.upper()}**: {valor}")
    print("---------------------------------")


def inserir_aluno(df):
    print("\n--- INSERIR NOVO ALUNO ---")

    novo_aluno = {}

    novo_aluno['Matricula'] = gerar_matricula(df)
    print(f"Matrícula gerada automaticamente: **{novo_aluno['Matricula']}**")
    

    campos_para_input = COLUNAS[1:] 

    for campo in campos_para_input:
        while True:
            valor = input(f"Digite o {campo} do aluno: ").strip()
            if valor:
                novo_aluno[campo] = valor
                break
            else:
                print(f"O campo {campo} não pode ser vazio. Tente novamente.")

    novo_df = pd.DataFrame([novo_aluno], columns=COLUNAS)
    

    df_atualizado = pd.concat([df, novo_df], ignore_index=True)
    
    if salvar_dataframe(df_atualizado):
        print(f"\n Aluno {novo_aluno['Nome']} cadastrado com SUCESSO! (Matrícula: {novo_aluno['Matricula']})")
    return df_atualizado

def pesquisar_e_gerenciar_aluno(df):

    print("\n--- PESQUISAR ALUNO ---")
    if df.empty:
        print("Ainda não há alunos cadastrados no sistema.")
        return df

    termo_busca = input("Digite o **Número de Matrícula** ou o **Nome** do aluno para pesquisar: ").strip()

    index_iloc, dados_aluno = buscar_aluno(df, termo_busca)

    if dados_aluno:
        exibir_dados_aluno(dados_aluno)
        
        while True:
            print("\nO que deseja fazer com este aluno?")
            escolha = input("**(E)**ditar / **(R)**emover / **(V)**oltar: ").strip().upper()
            
            if escolha == 'E':
                return editar_aluno(df, index_iloc, dados_aluno)
            elif escolha == 'R':
                return remover_aluno(df, index_iloc, dados_aluno)
            elif escolha == 'V':
                print("Voltando ao menu principal.")
                return df # Retorna o DF sem alteração
            else:
                print("Opção inválida. Digite E, R ou V.")

    else:
        print(f"\n Aluno com matrícula/nome '{termo_busca}' NÃO encontrado.")
        return df

def editar_aluno(df, index_iloc, dados_aluno):

    print("\n--- EDITAR DADOS DO ALUNO ---")
    
    campos_editaveis = {
        '1': 'Nome', 
        '2': 'Rua', 
        '3': 'Numero', 
        '4': 'Bairro', 
        '5': 'Cidade', 
        '6': 'UF', 
        '7': 'Telefone', 
        '8': 'Email'
    }
    campos_editaveis_lista = list(campos_editaveis.values())
    
    print("Selecione o dado que deseja editar:")
    for key, val in campos_editaveis.items():
        print(f"[{key}] {val} (Atual: {dados_aluno[val]})")
    print("[0] Cancelar Edição")
    
    while True:
        escolha_campo = input("Digite o número do campo a editar (1 a 8) ou 0 para cancelar: ").strip()
        
        if escolha_campo == '0':
            print("Edição cancelada. Voltando ao menu principal.")
            return df
        
        campo_a_editar = campos_editaveis.get(escolha_campo)
        if campo_a_editar:
            break
        else:
            print("Opção inválida.")
    
    while True:
        novo_valor = input(f"Digite o NOVO valor para **{campo_a_editar}**: ").strip()
        if novo_valor:
            break
        else:
            print(f"O campo {campo_a_editar} não pode ser vazio. Tente novamente.")
            
    df.loc[index_iloc, campo_a_editar] = novo_valor
    
    if salvar_dataframe(df):
        print(f"\n Dado '{campo_a_editar}' do aluno **{dados_aluno['Nome']}** atualizado com SUCESSO!")
        exibir_dados_aluno(df.loc[index_iloc].to_dict()) # Exibe os dados atualizados
    return df

def remover_aluno(df, index_iloc, dados_aluno):

    print("\n--- REMOVER ALUNO ---")
    
    confirmacao = input(f"Tem certeza que deseja **REMOVER** o aluno **{dados_aluno['Nome']}** (Matrícula: {dados_aluno['Matricula']})? [S/N]: ").strip().upper()
    
    if confirmacao == 'S':

        df_atualizado = df.drop(index=index_iloc).reset_index(drop=True)
        
        if salvar_dataframe(df_atualizado):
            print(f"\n Aluno **{dados_aluno['Nome']}** (Matrícula: {dados_aluno['Matricula']}) removido com SUCESSO!")
        return df_atualizado
    else:
        print("Remoção cancelada. Voltando ao menu principal.")
        return df


def menu_principal():

    alunos_df = inicializar_dataframe()

    while True:
        print("\n" + "="*40)
        print("TRABALHO PRÁTICO")
        print("CADASTRO DE ALUNOS")
        print("="*40)
        print("[1] INSERIR NOVO ALUNO")
        print("[2] PESQUISAR/EDITAR/REMOVER ALUNO")
        print("[3] SAIR")

        escolha = input("Selecione uma opção de (1 a 3): ").strip()

        if escolha == '1':
            alunos_df = inserir_aluno(alunos_df)
        
        elif escolha == '2':
            alunos_df = pesquisar_e_gerenciar_aluno(alunos_df)
            
        elif escolha == '3':
            print("\ O cadastro será encerrado. Até logo!")
            break
            
        else:
            print("\n Opção inválida. Por favor, escolha 1, 2 ou 3.")


if __name__ == "__main__":
    menu_principal()



