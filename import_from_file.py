#!/usr/bin/python3

import sys
import PyPDF2
import re
from datetime import datetime

def extrair_texto_de_pdf(caminho_do_arquivo):
    try:
        with open(caminho_do_arquivo, 'rb') as arquivo:
            leitor_pdf = PyPDF2.PdfReader(arquivo)
            texto_completo = []
            for pagina in leitor_pdf.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto_completo.append(texto_pagina)
            return "\n".join(texto_completo)
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        sys.exit(1)

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
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"dns_entries_{timestamp}.txt"
    with open(nome_arquivo, 'w') as file:
        file.write(dados)
    print(f"Resultado salvo em {nome_arquivo}")

def salvar_to_export(dados):
    nome_arquivo = "dns_entries.txt"
    with open(nome_arquivo, 'w') as file:
        file.write(dados)
    print(f"Resultado salvo em {nome_arquivo}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 script.py <caminho_do_PDF>")
        sys.exit(1)

    caminho_pdf = sys.argv[1]
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
