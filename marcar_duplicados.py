import pandas as pd
import argparse
import re

def limpar_string_telefone(telefone_str):
    telefone_str = str(telefone_str)
    telefone_str = telefone_str.replace(' ', '')
    telefone_str = re.sub(r'[^0-9:]', '', telefone_str)
    telefone_str = re.sub(r':+', ':::', telefone_str)
    return telefone_str

def parse_number(numero):
    indice = numero.find('9')
    
    if indice != -1:
        return numero[indice + 1:]
    else:
        return numero

def get_numeros(row):
    numeros = []
    string_numero1 = limpar_string_telefone(row['Phone 1 - Value'])
    numeros1 = string_numero1.split(':::')
    numeros1 = [numero for numero in numeros1 if numero]
    for numero in numeros1:
        numeros.append(numero)
    
    if pd.notna(row['Phone 2 - Value']):
        string_numero2 = limpar_string_telefone(row['Phone 2 - Value'])
        numeros2 = string_numero2.split(':::')
        numeros2 = [numero for numero in numeros2 if numero]
        for numero in numeros2:
            numeros.append(numero)
    
    for numero in numeros:
        parse_number(numero)
        
    return numeros

def tem_numero_repetido(numeros1, numeros2):
    for numero in numeros1:
        if numero in numeros2:
            return True
    return False

def main(caminho_contatos_original, caminho_contatos_novos):
    df_original = pd.read_csv(caminho_contatos_original)
    df_novos = pd.read_csv(caminho_contatos_novos)

    df_original = df_original.dropna(subset=['First Name'])
    
    df_novos['Repetido?'] = 0
    
    lista_numeros_original = []
    
    for _, row_original in df_original.iterrows():
        lista_numeros_original.append(get_numeros(row_original));        
    
    for i, row_novos in df_novos.iterrows():
        numeros_novo = get_numeros(row_novos)
        for numeros_original in lista_numeros_original:
            if tem_numero_repetido(numeros_novo, numeros_original):
                df_novos.at[i, 'Repetido?'] = 1
                break

    novo_caminho_planilha = 'contatos_marcados.csv'
    print(df_novos)
    df_novos.to_csv(novo_caminho_planilha, index=False)

    print(f'\nA planilha com os contatos marcados foi salva em "{novo_caminho_planilha}".')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Marcar todas as entradas da planilha de contatos_novos cujos nuemros\
                                     de telefone tem alguma correspondencia nos numeros existentes na planilha de contatos_original\
                                         . OBS: contatos PRECISAM começar com o dígito 9')
    parser.add_argument('caminho_contatos_original', type=str, help='Caminho para o arquivo CSV com os contatos originais')
    parser.add_argument('caminho_contatos_novos', type=str, help='Caminho para o arquivo CSV com os contatos novos')

    args = parser.parse_args()

    main(args.caminho_contatos_original, args.caminho_contatos_novos)