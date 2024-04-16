#!/usr/bin/python3

# apt update
# apt upgrade
# apt install python3-full
# apt install python3-flask
# apt install gunicorn
# apt install uwsgi

# mkdir /anatel
# cd /anatel/
# apt autoremove
# apt install python3-full
# pip install PyPDF2
# apt install python3-pypdf
# apt install python3-pypdf2
# apt install python3-requests
# apt install python3-venv
# python3 -m venv  /anatel/env
# source /anatel/env/bin/activate
# pip install PyPDF2
# apt install pipx
# pipx ensurepath
# pipx install PyPDF2
# pip install requests
# 

# Usage:
# ./import_from_url.py  https://sistemas.anatel.gov.br/anexar-api/publico/anexos/download/5e68ae83f4826fdb20f8f553447008f3


import sys
import requests
import PyPDF2
import re
import tempfile
from datetime import datetime

def baixar_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem sucedida
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(response.content)
            return tmp.name  # Retorna o nome do arquivo temporário
    except requests.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
        sys.exit(1)

def extrair_texto_de_pdf(caminho_do_arquivo):
    with open(caminho_do_arquivo, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = []
        for pagina in leitor_pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_completo.append(texto_pagina)
        return "\n".join(texto_completo)

def gerar_entradas_dns(url):
    dominio = re.findall(r"\b(?:http(?:s)?://)?(\w+[\w\-\.]+(?:\.\w+)+)\b", url)
    if dominio:
        return f"{dominio[0]} IN CNAME .\n*{dominio[0]} IN CNAME ."
    return ""

def imprimir_cabecalho_dns():
    serial = datetime.now().strftime("%Y%m%d%H")
    header = f"$TTL 1H\n@       IN      SOA LOCALHOST. localhost.localhost. (\n                {serial}      ; Serial\n                1h              ; Refresh\n                15m             ; Retry\n                30d             ; Expire\n                2h              ; Negative Cache TTL\n        )\n        NS  localhost."
    print(header)
    return header

def salvar_resultados_no_arquivo(dados):
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    nome_arquivo = f"dns_entries_{timestamp}.txt"
    with open(nome_arquivo, 'w') as file:
        file.write(dados)
    print(f"Resultado salvo em {nome_arquivo}")  # Remove as aspas simples da mensagem
    
def salvar_to_export(dados):    
    nome_arquivo = f"dns_entries.txt"
    with open(nome_arquivo, 'w') as file:
        file.write(dados)
    print(f"Resultado salvo em {nome_arquivo}")  # Remove as aspas simples da mensagem    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 script.py <URL_do_PDF>")
        sys.exit(1)

    url_pdf = sys.argv[1]
    caminho_pdf = baixar_pdf(url_pdf)
    texto_extraido = extrair_texto_de_pdf(caminho_pdf)

    regex_urls = r"\b(?:http(?:s)?://)?\w+[\w\-\.]+(?:\.\w+)+\b"
    urls_encontradas = re.findall(regex_urls, texto_extraido)
    urls_filtradas = [url for url in urls_encontradas if not any(proibido in url.lower() for proibido in ["policia", ".gov"])]

    cabecalho_dns = imprimir_cabecalho_dns()
    resultado_dns = cabecalho_dns + "\n"

    for url in urls_filtradas:
        entradas_dns = gerar_entradas_dns(url)
        print(entradas_dns)
        resultado_dns += entradas_dns + "\n"

    # Salvar o resultado em um arquivo com timestamp
    salvar_resultados_no_arquivo(resultado_dns)
    salvar_to_export(resultado_dns)
