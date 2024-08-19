import pandas as pd
import numpy as np
import argparse

def adicionar_prefixo(row, prefixo):
    print(row['First Name'])
    print(row['Distrito'])
    
    if pd.isna(row['Distrito']) or pd.isna(row['First Name']):
        return row['First Name'] if pd.notna(row['First Name']) else np.nan
    else:
        distrito_str = str(int(row['Distrito'])) if pd.notna(row['Distrito']) else ''
        return prefixo + '_Dist_' + distrito_str + '_' + row['First Name']

def main(caminho_planilha, prefixo):
    df = pd.read_csv(caminho_planilha)

    df = df.dropna(subset=['First Name'])

    df['First Name'] = df.apply(adicionar_prefixo, axis=1, prefixo=prefixo)

    df = df.drop(columns=['Distrito'])

    print(df)

    novo_caminho_planilha = 'contatos_renomeados.csv'

    df.to_csv(novo_caminho_planilha, index=False)

    print(f'\nA planilha com os contatos renomeados foi salva em "{novo_caminho_planilha}".')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Renomear os contatos da planilha de acordo com um prefixo')
    parser.add_argument('caminho_planilha', type=str, help='Caminho para o arquivo CSV de entrada')
    parser.add_argument('prefixo', type=str, help='Prefixo a ser adicionado ao nome')

    args = parser.parse_args()

    main(args.caminho_planilha, args.prefixo)