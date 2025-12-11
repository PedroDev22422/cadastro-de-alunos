--O código serve para realizar cadastro de alunos onde ficará armazenado em um mini banco de dados--

--Para executar o código corretamente, será necesário importar a biblioteca pandas e a os. Também será necessário  ter instalado o java, python e o pandas em sua máquina para não ocorrer erros na execução--

--Autores--
Pedro Henrique Canto da Silva,
Lucas Ribeiro Dias


--Explicação das linhas de código--

import pandas as pd
import os

# --- Configurações Globais ---
ARQUIVO_CSV = 'alunos.csv'

COLUNAS = ['Matricula', 'Nome', 'Rua', 'Numero', 'Bairro', 'Cidade', 'UF', 'Telefone', 'Email']

# --- Funções de Utilitários e Gerenciamento de Arquivo ---

def inicializar_dataframe():
    """
    Tenta carregar o DataFrame do arquivo CSV. Se o arquivo não existir,
    cria um novo DataFrame vazio.
    Retorna o DataFrame.
    """
    try:
        # Tenta ler o arquivo CSV
        df = pd.read_csv(ARQUIVO_CSV)
        # Garante que a coluna 'Matricula' seja tratada como inteiro
        df['Matricula'] = df['Matricula'].astype(int)
    except FileNotFoundError:
        # Se o arquivo não existir, cria um DataFrame vazio com as colunas definidas
        df = pd.DataFrame(columns=COLUNAS)
        print(f"Arquivo '{ARQUIVO_CSV}' não encontrado. Criando um novo sistema de cadastro.")
    except pd.errors.EmptyDataError:
        # Se o arquivo existir, mas estiver vazio
        df = pd.DataFrame(columns=COLUNAS)
        print(f"Arquivo '{ARQUIVO_CSV}' está vazio. Iniciando um novo cadastro.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        df = pd.DataFrame(columns=COLUNAS) # Cria um DF vazio como fallback
    return df

def salvar_dataframe(df):
    """
    Salva o DataFrame atual no arquivo CSV.
    """
    try:
        # Salva o DataFrame no arquivo CSV, sem o índice
        df.to_csv(ARQUIVO_CSV, index=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")
        return False

def gerar_matricula(df):
    """
    Gera um novo número de matrícula sequencial.
    Se o DataFrame estiver vazio, a primeira matrícula é 1.
    Caso contrário, é o último valor + 1.
    """
    if df.empty:
        return 1
    else:
        # Encontra o valor máximo da coluna 'Matricula' e adiciona 1
        return df['Matricula'].max() + 1

def buscar_aluno(df, termo_busca):
    """
    Pesquisa um aluno por número de matrícula (int) ou nome (case-insensitive).
    Retorna o índice (iloc) do aluno no DataFrame ou None se não for encontrado.
    """
    if df.empty:
        return None, None

    try:
        # Tenta buscar por Matrícula (tratada como int)
        matricula = int(termo_busca)
        # Filtra o DataFrame onde a 'Matricula' é igual ao termo_busca
        resultado = df[df['Matricula'] == matricula]
        if not resultado.empty:
            # Retorna o índice iloc (posição) e os dados do aluno como um dicionário
            return resultado.index[0], resultado.iloc[0].to_dict()

    except ValueError:
        # Se a conversão para int falhar, busca por Nome (case-insensitive)
        nome = str(termo_busca).strip()
        # Converte a coluna 'Nome' e o termo de busca para minúsculas antes de comparar
        # .str.lower() é usado para aplicar a função de string em toda a coluna
        resultado = df[df['Nome'].str.lower() == nome.lower()]
        if not resultado.empty:
            # Retorna o índice iloc do primeiro resultado e seus dados
            return resultado.index[0], resultado.iloc[0].to_dict()

    # Se a busca não encontrou nada
    return None, None

def exibir_dados_aluno(dados):
    """
    Apresenta os dados de um aluno formatados na tela.
    Recebe um dicionário com os dados do aluno.
    """
    print("\n--- DADOS DO ALUNO ENCONTRADO ---")
    for chave, valor in dados.items():
        print(f"**{chave.upper()}**: {valor}")
    print("---------------------------------")

# --- Funções do Menu Principal ---

def inserir_aluno(df):
    """
    Solicita os dados do novo aluno, gera a matrícula e adiciona ao DataFrame.
    """
    print("\n--- INSERIR NOVO ALUNO ---")

    # Dicionário temporário para armazenar os dados do novo aluno
    novo_aluno = {}
    
    # Gera a matrícula automaticamente
    novo_aluno['Matricula'] = gerar_matricula(df)
    print(f"Matrícula gerada automaticamente: **{novo_aluno['Matricula']}**")
    
    # Lista dos campos que o usuário deve preencher (exceto Matrícula)
    campos_para_input = COLUNAS[1:] 

    for campo in campos_para_input:
        # Loop para garantir que o usuário preencha o campo (não vazio)
        while True:
            valor = input(f"Digite o {campo} do aluno: ").strip()
            if valor:
                novo_aluno[campo] = valor
                break
            else:
                print(f"O campo {campo} não pode ser vazio. Tente novamente.")

    # Converte o dicionário do novo aluno em um DataFrame de uma linha
    novo_df = pd.DataFrame([novo_aluno], columns=COLUNAS)
    
    # Adiciona o novo registro ao DataFrame principal
    # pd.concat é o método moderno para combinar DataFrames
    df_atualizado = pd.concat([df, novo_df], ignore_index=True)
    
    # Salva e retorna o DataFrame atualizado
    if salvar_dataframe(df_atualizado):
        print(f"\n Aluno {novo_aluno['Nome']} cadastrado com SUCESSO! (Matrícula: {novo_aluno['Matricula']})")
    return df_atualizado

def pesquisar_e_gerenciar_aluno(df):
    """
    Busca um aluno e, se encontrado, pergunta se o usuário deseja Editar ou Remover.
    """
    print("\n--- PESQUISAR ALUNO ---")
    if df.empty:
        print("Ainda não há alunos cadastrados no sistema.")
        return df

    termo_busca = input("Digite o **Número de Matrícula** ou o **Nome** do aluno para pesquisar: ").strip()

    # Busca o aluno
    index_iloc, dados_aluno = buscar_aluno(df, termo_busca)

    if dados_aluno:
        exibir_dados_aluno(dados_aluno)
        
        # Oferece as opções de gerencimento
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
        return df # Retorna o DF sem alteração

def editar_aluno(df, index_iloc, dados_aluno):
    """
    Permite ao usuário editar um dado específico do aluno.
    """
    print("\n--- EDITAR DADOS DO ALUNO ---")
    
    # Dicionário de mapeamento dos campos editáveis para exibição
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
    
    # Apresenta o menu de edição
    print("Selecione o dado que deseja editar:")
    for key, val in campos_editaveis.items():
        print(f"[{key}] {val} (Atual: {dados_aluno[val]})")
    print("[0] Cancelar Edição")
    
    while True:
        escolha_campo = input("Digite o número do campo a editar (1-8) ou 0 para cancelar: ").strip()
        
        if escolha_campo == '0':
            print("Edição cancelada. Voltando ao menu principal.")
            return df
        
        campo_a_editar = campos_editaveis.get(escolha_campo)
        if campo_a_editar:
            break
        else:
            print("Opção inválida.")
    
    # Solicita o novo valor para o campo escolhido
    while True:
        novo_valor = input(f"Digite o NOVO valor para **{campo_a_editar}**: ").strip()
        if novo_valor:
            break
        else:
            print(f"O campo {campo_a_editar} não pode ser vazio. Tente novamente.")
            
    # Aplica a alteração diretamente no DataFrame usando .loc
    # loc[index_iloc, campo_a_editar] acessa a célula específica para edição
    df.loc[index_iloc, campo_a_editar] = novo_valor
    
    # Salva e retorna o DataFrame atualizado
    if salvar_dataframe(df):
        print(f"\n Dado '{campo_a_editar}' do aluno **{dados_aluno['Nome']}** atualizado com SUCESSO!")
        exibir_dados_aluno(df.loc[index_iloc].to_dict()) # Exibe os dados atualizados
    return df

def remover_aluno(df, index_iloc, dados_aluno):
    """
    Remove um aluno do DataFrame após confirmação.
    """
    print("\n--- REMOVER ALUNO ---")
    
    confirmacao = input(f"Tem certeza que deseja **REMOVER** o aluno **{dados_aluno['Nome']}** (Matrícula: {dados_aluno['Matricula']})? [S/N]: ").strip().upper()
    
    if confirmacao == 'S':
        # Remove a linha usando o índice iloc
        # axis=0 indica que estamos removendo uma linha
        df_atualizado = df.drop(index=index_iloc).reset_index(drop=True)
        
        # Salva e retorna o DataFrame atualizado
        if salvar_dataframe(df_atualizado):
            print(f"\n Aluno **{dados_aluno['Nome']}** (Matrícula: {dados_aluno['Matricula']}) removido com SUCESSO!")
        return df_atualizado
    else:
        print("Remoção cancelada. Voltando ao menu principal.")
        return df # Retorna o DF sem alteração

# --- Função Principal do Programa ---

def menu_principal():
    """
    Função principal que gerencia o loop do menu do programa.
    """
    # Carrega os dados existentes (ou cria um DF novo) ao iniciar o programa
    alunos_df = inicializar_dataframe()

    while True:
        print("\n" + "="*40)
        print("TRABALHO PRÁTICO")
        print("CADASTRO DE ALUNOS")
        print("="*40)
        print("[1] INSERIR NOVO ALUNO")
        print("[2] PESQUISAR/EDITAR/REMOVER ALUNO")
        print("[3] SAIR")

        # Trata a entrada do usuário
        escolha = input("Selecione uma opção (1-3): ").strip()

        if escolha == '1':
            # Chama a função de inserir e atualiza o DataFrame principal
            alunos_df = inserir_aluno(alunos_df)
        
        elif escolha == '2':
            # Chama a função de pesquisa/gerenciamento e atualiza o DataFrame
            alunos_df = pesquisar_e_gerenciar_aluno(alunos_df)
            
        elif escolha == '3':
            print("\ O programa será encerrado. Até logo!")
            break
            
        else:
            print("\n Opção inválida. Por favor, escolha 1, 2 ou 3.")

# --- Execução do Programa ---

if __name__ == "__main__":

    menu_principal()

