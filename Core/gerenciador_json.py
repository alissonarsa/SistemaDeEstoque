import json
import os
from Models.produto import Produto
from Models.engradado import Engradado
from Estrutura.pilha import Pilha
from Core.estoque import Estoque
from Estrutura.fila import Fila
from Models.pedido import Pedido, ItemPedido

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

# salva o estado completo do sistema (estoque, fila, histórico) em um arquivo JSON
def salvar_estado_sistema(estoque: Estoque, fila: Fila, historico: list):
    print("\nSalvando estado do sistema...")
    estado_completo = {
        "estoque": estoque.to_dict(),
        "fila_de_pedidos": fila.to_dict(),
        "historico_de_pedidos": [p.to_dict() for p in historico]
    }
    with open(ESTADO_SISTEMA_PATH, 'w', encoding='utf-8') as f:
        json.dump(estado_completo, f, indent=4, ensure_ascii=False)
    print("Estado do sistema salvo com sucesso!")

# carrega o estado completo do sistema. Se não houver estado salvo, retorna objetos novos
def carregar_estado_sistema() -> (Estoque, Fila, list):
    print("Carregando estado do sistema...")
    try:
        with open(ESTADO_SISTEMA_PATH, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        dados_estoque = dados['estoque']
        estoque_carregado = Estoque(linhas=dados_estoque['linhas'], colunas=dados_estoque['colunas'])
        for i, linha in enumerate(dados_estoque['layout']):
            for j, p_dict in enumerate(linha):
                pilha = Pilha(p_dict['capacidade'])
                for e_dict in p_dict['itens']:
                    prod_obj = Produto(**e_dict['produto'])
                    eng_obj = Engradado(prod_obj, e_dict['quantidade_maxima'])
                    eng_obj.quantidade_atual = e_dict['quantidade_atual']
                    pilha.empilhar(eng_obj)
                estoque_carregado.layout[i][j] = pilha
        estoque_carregado.mapa_produtos = {k: [tuple(v) for v in val] for k, val in dados_estoque['mapa_produtos'].items()}

        fila_carregada = Fila()
        for ped_dict in dados['fila_de_pedidos']['itens']:
            pedido_obj = Pedido(ped_dict['nome_solicitante'])
            pedido_obj.data_solicitacao = datetime.date.fromisoformat(ped_dict['data_solicitacao'])
            for item_dict in ped_dict['itens_pedido']:
                pedido_obj.adicionar_item(item_dict['codigo_produto'], item_dict['quantidade'])
            fila_carregada.enfileirar(pedido_obj)
            
        historico_carregado = []
        for ped_dict in dados['historico_de_pedidos']:
             pedido_obj = Pedido(ped_dict['nome_solicitante'])
             historico_carregado.append(pedido_obj)

        print("Estado do sistema carregado com sucesso!")
        return estoque_carregado, fila_carregada, historico_carregado

    except (FileNotFoundError, KeyError):
        print("Nenhum estado salvo encontrado. Iniciando um sistema novo.")
        return Estoque(), Fila(), []