#!/anatel/env/bin/python3

import PyPDF2
import re
import sys
from datetime import datetime

def extrair_texto_de_pdf(caminho_do_arquivo):
    # Abrir o arquivo PDF em modo leitura binária
    with open(caminho_do_arquivo, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = []

        # Iterar sobre cada página no arquivo PDF
        for pagina in leitor_pdf.pages:
            # Extrair texto da página atual
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo.append(texto_pagina)

        # Unir todos os textos extraídos em uma única string
        return "\n".join(texto_completo)

def gerar_entradas_dns(url):
    # Extrair o domínio principal da URL
    dominio = re.findall(r"\b(?:http(?:s)?://)?(\w+[\w\-\.]+(?:\.\w+)+)\b", url)
    if dominio:
        # Retorna entradas CNAME para o domínio e para o wildcard '*'
        return f"{dominio[0]} IN CNAME .\n*{dominio[0]} IN CNAME ."
    return ""

def gerar_cabecalho_dns():
    # Gerar serial com base na data e hora atual
    data_atual = datetime.now()
    serial = data_atual.strftime("%Y%m%d%H")
    cabecalho = f"""$TTL 1H
@       IN      SOA LOCALHOST. localhost.localhost. (
                {serial}      ; Serial
                1h            ; Refresh
                15m           ; Retry
                30d           ; Expire
                2h            ; Negative Cache TTL
        )
        NS  localhost."""
    return cabecalho

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 script.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_do_arquivo = sys.argv[1]
    texto_extraido = extrair_texto_de_pdf(caminho_do_arquivo)

    # Expressão regular para encontrar URLs
    regex_urls = r"\b(?:http(?:s)?://)?\w+[\w\-\.]+(?:\.\w+)+\b"
    urls_encontradas = re.findall(regex_urls, texto_extraido)

    # Filtrar URLs que contêm 'policia' ou '.gov'
    urls_filtradas = [url for url in urls_encontradas if not any(proibido in url.lower() for proibido in ["policia", ".gov"])]

    # Gerar e imprimir o cabeçalho DNS
    print(gerar_cabecalho_dns())

    # Gerar e imprimir as entradas DNS para cada URL filtrada
    for url in urls_filtradas:
        entradas_dns = gerar_entradas_dns(url)
        print(entradas_dns)
