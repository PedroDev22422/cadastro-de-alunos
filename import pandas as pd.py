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
        df = pd.DataFrame(columns=COLUNAS)
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
                return df
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
        escolha_campo = input("Digite o número do campo a editar (1-8) ou 0 para cancelar: ").strip()
        
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
        exibir_dados_aluno(df.loc[index_iloc].to_dict()) 
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

        escolha = input("Selecione uma opção (1-3): ").strip()

        if escolha == '1':
            alunos_df = inserir_aluno(alunos_df)
        
        elif escolha == '2':
            alunos_df = pesquisar_e_gerenciar_aluno(alunos_df)
            
        elif escolha == '3':
            print("\ O programa será encerrado. Até logo!")
            break
            
        else:
            print("\n Opção inválida. Por favor, escolha 1, 2 ou 3.")


if __name__ == "__main__":

    menu_principal()
