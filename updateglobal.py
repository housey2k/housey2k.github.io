import os
import re

OLD_SCRIPT_TAG = '<script src="analytics.js"></script>'
NEW_SCRIPT_TAG = '  <script src="/analytics.js"></script>\n'

# Se quiser excluir footer.html, mantenha aqui:
EXCLUDE_FILES = {'footer.html', 'header.html'}

def corrigir_ou_inserir_script(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    alterado = False

    # Remove tag antiga, se existir
    if OLD_SCRIPT_TAG in conteudo:
        conteudo = conteudo.replace(OLD_SCRIPT_TAG, '')
        alterado = True
        print(f'Tag antiga removida em: {caminho_arquivo}')

    # Verifica se já tem a nova tag
    if NEW_SCRIPT_TAG.strip() not in conteudo:
        if '</head>' in conteudo:
            conteudo = conteudo.replace('</head>', NEW_SCRIPT_TAG + '</head>')
            alterado = True
            print(f'Tag nova inserida antes de </head> em: {caminho_arquivo}')
        elif '<head>' in conteudo:
            conteudo = conteudo.replace('<head>', '<head>\n' + NEW_SCRIPT_TAG)
            alterado = True
            print(f'Tag nova inserida após <head> em: {caminho_arquivo}')
        else:
            conteudo = NEW_SCRIPT_TAG + conteudo
            alterado = True
            print(f'Tag nova inserida no início do arquivo: {caminho_arquivo}')
    else:
        if not alterado:
            print(f'Arquivo já possui a tag correta: {caminho_arquivo}')

    if alterado:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)

def main():
    raiz = '.'

    for root, dirs, files in os.walk(raiz):
        for file in files:
            if file.endswith('.html') and file not in EXCLUDE_FILES:
                caminho = os.path.join(root, file)
                corrigir_ou_inserir_script(caminho)

if __name__ == '__main__':
    main()
