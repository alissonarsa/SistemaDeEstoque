import json
import os
from Models.produto import Produto
from Core.estoque import Estoque

CAMINHO_CATALOGO = 'catalogo_produtos.json'
ESTADO_SISTEMA_PATH = 'estado_sistema.json'

def _ler_catalogo():
    """Função auxiliar (privada) para ler os dados do arquivo JSON."""
    if not os.path.exists(CAMINHO_CATALOGO):
        return []
    try:
        with open(CAMINHO_CATALOGO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _salvar_catalogo(produtos):
    """Função auxiliar (privada) para salvar a lista de produtos no arquivo JSON."""
    with open(CAMINHO_CATALOGO, 'w', encoding='utf-8') as f:
        json.dump(produtos, f, indent=4, ensure_ascii=False)

def listar_produtos():
    """Retorna a lista de todos os produtos do catálogo."""
    return _ler_catalogo()

def adicionar_produto(novo_produto):
    """Adiciona um novo produto ao catálogo."""
    produtos = _ler_catalogo()
    for p in produtos:
        if p['codigo'] == novo_produto['codigo']:
            print(f"ERRO: Código de produto '{novo_produto['codigo']}' já existe.")
            return
    produtos.append(novo_produto)
    _salvar_catalogo(produtos)

def remover_produto_por_codigo(codigo):
    """Remove um produto do catálogo usando seu código."""
    produtos = _ler_catalogo()
    produtos_atualizados = [p for p in produtos if p['codigo'] != codigo]
    if len(produtos_atualizados) < len(produtos):
        _salvar_catalogo(produtos_atualizados)
        return True
    return False

def alterar_produto(codigo, dados_para_alterar):
    """Altera um ou mais campos de um produto existente."""
    produtos = _ler_catalogo()
    produto_encontrado = False
    for produto in produtos:
        if produto['codigo'] == codigo:
            produto.update(dados_para_alterar)
            produto_encontrado = True
            break
    if produto_encontrado:
        _salvar_catalogo(produtos)
    return produto_encontrado

def salvar_estado_estoque(estoque: Estoque):
    """
    Salva o estado atual do objeto Estoque em um arquivo JSON.
    """
    print("\nSalvando estado do estoque...")
    dados_estoque = estoque.to_dict()
    with open(ESTADO_SISTEMA_PATH, 'w', encoding='utf-8') as f:
        json.dump(dados_estoque, f, indent=4, ensure_ascii=False)
    print("Estado do estoque salvo com sucesso!")