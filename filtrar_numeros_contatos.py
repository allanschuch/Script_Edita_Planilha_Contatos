import pandas as pd
import argparse
import re

def limpar_string_telefone(telefone_str):
    telefone_str = str(telefone_str)
    telefone_str = telefone_str.replace(' ', '')
    telefone_str = re.sub(r'[^0-9:]', '', telefone_str)
    telefone_str = re.sub(r':+', ':::', telefone_str)
    return telefone_str

def avalia_numero(row, cod_area, cod_tel_fixo):
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
        if len(numero) <= 9:
            if len(numero) < 8:
                return False
            if cod_tel_fixo in numero[:5]:
                return False 
            else:
                return True
        else:
            if cod_area in numero[:5]:
                return True   
    return False
           

def main(caminho_planilha, cod_area, cod_tel_fixo):
    df = pd.read_csv(caminho_planilha)
    
    df = df.dropna(subset=['First Name'])
    
    mascara = df.apply(avalia_numero, axis=1, cod_area=cod_area, cod_tel_fixo=cod_tel_fixo)
    
    #pd.set_option('display.max_columns', None)  # Mostra todas as colunas
    pd.set_option('display.max_rows', None)     # Mostra todas as linhas

    print(mascara)

    df_filtrado = df[mascara]

    novo_caminho_planilha = 'contatos_filtrados.csv'

    df_filtrado.to_csv(novo_caminho_planilha, index=False)
    
    print(df_filtrado)

    print(f'A planilha com os números removidos foi salva em "{novo_caminho_planilha}".')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remover todas as entradas da lista de contatos que contém o código de área informado, que sejam menores que 8 digitos ou \
                                     que comecem com o codigo de telefone fixo informado')
    parser.add_argument('caminho_planilha', type=str, help='Caminho para o arquivo CSV de entrada')
    parser.add_argument('cod_area', type=str, help='Código de área a ser procurado para remover as entradas que o contém')
    parser.add_argument('cod_tel_fixo', type=str, help='Código de telefone fixo a ser procurado para remover as entradas que o contém')

    args = parser.parse_args()

    main(args.caminho_planilha, args.cod_area, args.cod_tel_fixo)