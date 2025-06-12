# Arquivo: Core/gerenciador_json.py
# Descrição: Funções para gerenciar o catálogo de produtos em JSON.

import json
import os

# Define o nome do arquivo como uma constante para fácil manutenção
CAMINHO_CATALOGO = 'catalogo_produtos.json'

def _ler_catalogo():
    """Função auxiliar (privada) para ler os dados do arquivo JSON."""
    if not os.path.exists(CAMINHO_CATALOGO):
        return []  # Retorna lista vazia se o arquivo não existe
    try:
        with open(CAMINHO_CATALOGO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return [] # Retorna lista vazia se o arquivo estiver vazio ou corrompido

def _salvar_catalogo(produtos):
    """Função auxiliar (privada) para salvar a lista de produtos no arquivo JSON."""
    with open(CAMINHO_CATALOGO, 'w', encoding='utf-8') as f:
        # json.dump escreve os dados no arquivo. indent=4 formata o arquivo para ser legível.
        json.dump(produtos, f, indent=4, ensure_ascii=False)

def listar_produtos():
    """Retorna a lista de todos os produtos do catálogo."""
    return _ler_catalogo()

def adicionar_produto(novo_produto):
    """Adiciona um novo produto ao catálogo."""
    produtos = _ler_catalogo()
    # Verifica se o código do produto já existe
    for p in produtos:
        if p['codigo'] == novo_produto['codigo']:
            print(f"ERRO: Código de produto '{novo_produto['codigo']}' já existe.")
            return
    produtos.append(novo_produto)
    _salvar_catalogo(produtos)

def remover_produto_por_codigo(codigo):
    """Remove um produto do catálogo usando seu código."""
    produtos = _ler_catalogo()
    produto_encontrado = False
    # Cria uma nova lista sem o produto a ser removido
    produtos_atualizados = [p for p in produtos if p['codigo'] != codigo]
    
    if len(produtos_atualizados) < len(produtos):
        produto_encontrado = True
        _salvar_catalogo(produtos_atualizados)
        
    return produto_encontrado

def alterar_produto(codigo, dados_para_alterar):
    """Altera um ou mais campos de um produto existente."""
    produtos = _ler_catalogo()
    produto_encontrado = False
    for produto in produtos:
        if produto['codigo'] == codigo:
            # .update() mescla os dicionários, alterando os campos existentes
            produto.update(dados_para_alterar)
            produto_encontrado = True
            break
            
    if produto_encontrado:
        _salvar_catalogo(produtos)
        
    return produto_encontrado