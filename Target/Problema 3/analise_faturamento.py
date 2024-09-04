import xml.etree.ElementTree as ET
import json
import os

# Função para ler e extrair dados do XML
def ler_dados_xml(arquivo_xml):
    try:
        tree = ET.parse(arquivo_xml)
        root = tree.getroot()
        valores = []
        for row in root.findall('row'):
            valor = row.find('valor').text
            if valor:
                try:
                    valor = float(valor)
                    if valor > 0:  # Ignorar dias sem faturamento
                        valores.append(valor)
                except ValueError:
                    continue
        return valores
    except ET.ParseError as e:
        print(f"Erro ao parsear o XML: {e}")
        raise

# Função para ler e extrair dados do JSON
def ler_dados_json(arquivo_json):
    try:
        with open(arquivo_json, 'r') as f:
            dados = json.load(f)
        valores = [item['valor'] for item in dados if item['valor'] > 0]
        return valores
    except json.JSONDecodeError as e:
        print(f"Erro ao parsear o JSON: {e}")
        raise
    except FileNotFoundError as e:
        print(f"Arquivo JSON não encontrado: {e}")
        raise

# Função para calcular menor, maior e média
def calcular_faturamento(valores):
    if not valores:
        raise ValueError("Não há dados de faturamento disponíveis.")
    menor = min(valores)
    maior = max(valores)
    media = sum(valores) / len(valores)
    return menor, maior, media

# Função para contar dias com faturamento superior à média
def contar_dias_acima_da_media(valores, media):
    return len([v for v in valores if v > media])

# Função principal de análise
def analisar_faturamento():
    # Caminhos dos arquivos
    caminho_xml = 'dados.xml'
    caminho_json = 'dados.json'

    if not os.path.isfile(caminho_xml):
        raise FileNotFoundError(f"O arquivo XML '{caminho_xml}' não foi encontrado.")
    if not os.path.isfile(caminho_json):
        raise FileNotFoundError(f"O arquivo JSON '{caminho_json}' não foi encontrado.")

    # Carregar dados
    valores_xml = ler_dados_xml(caminho_xml)
    valores_json = ler_dados_json(caminho_json)

    # Combinar dados
    valores_combinados = valores_xml + valores_json

    # Calcular estatísticas
    menor, maior, media = calcular_faturamento(valores_combinados)
    dias_acima_da_media = contar_dias_acima_da_media(valores_combinados, media)

    # Exibir resultados
    print(f"Menor valor de faturamento: R$ {menor:.2f}")
    print(f"Maior valor de faturamento: R$ {maior:.2f}")
    print(f"Dias com faturamento acima da média: {dias_acima_da_media}")

if __name__ == '__main__':
    try:
        analisar_faturamento()
    except Exception as e:
        print(f"Erro: {e}")
