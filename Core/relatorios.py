import datetime
from Core.estoque import Estoque
from typing import List

def verificar_vencimento_recursivo(estoque: Estoque, linha: int, coluna: int, produtos_vencendo: List):
    # brek da recursividade
    if linha >= estoque.linhas:
        return

    pilha_atual = estoque.layout[linha][coluna]
    if not pilha_atual.esta_vazia():
        produto = pilha_atual.ver_topo().produto
        hoje = datetime.date.today()
        dias_para_vencer = (produto.data_validade - hoje).days
        
        # produto vence nos próximos 30 dias?
        if 0 <= dias_para_vencer <= 30 and produto not in produtos_vencendo:
            produtos_vencendo.append(produto)

    proxima_coluna = coluna + 1
    proxima_linha = linha
    if proxima_coluna >= estoque.colunas:
        proxima_coluna = 0
        proxima_linha += 1
        
    # rec.
    verificar_vencimento_recursivo(estoque, proxima_linha, proxima_coluna, produtos_vencendo)

def gerar_relatorio_vencimento(estoque: Estoque):
    print("\n--- RELATÓRIO: PRODUTOS PRÓXIMOS AO VENCIMENTO (30 dias) ---")
    produtos_vencendo = []
    verificar_vencimento_recursivo(estoque, 0, 0, produtos_vencendo)
    
    if not produtos_vencendo:
        print("Nenhum produto próximo ao vencimento.")
    else:
        for produto in produtos_vencendo:
            print(f" - Produto: {produto.nome} (Código: {produto.codigo}), Vence em: {produto.data_validade.strftime('%d/%m/%Y')}")
    print("----------------------------------------------------------")

def verificar_falta_recursivo(estoque: Estoque, lista_codigos_produto: List[str], produtos_em_falta: List[str]):
    if not lista_codigos_produto:
        return
        
    codigo = lista_codigos_produto[0]
    esta_em_falta = True
    
    # tem engradado disponivel para esse produto?
    for linha, coluna in estoque.mapa_produtos.get(codigo, []):
        if not estoque.layout[linha][coluna].esta_vazia():
            esta_em_falta = False
            break
            
    if esta_em_falta:
        produtos_em_falta.append(codigo)
        
    # rec.
    verificar_falta_recursivo(estoque, lista_codigos_produto[1:], produtos_em_falta)

def gerar_relatorio_itens_em_falta(estoque: Estoque):
    """Gera o relatório de produtos cadastrados mas sem estoque disponível."""
    print("\n--- RELATÓRIO: ITENS EM FALTA NO ESTOQUE ---")
    produtos_em_falta = []
    codigos_a_verificar = list(estoque.mapa_produtos.keys())
    verificar_falta_recursivo(estoque, codigos_a_verificar, produtos_em_falta)
    
    if not produtos_em_falta:
        print("Nenhum item em falta.")
    else:
        for codigo in produtos_em_falta:
            print(f" - Produto com código '{codigo}' está sem estoque disponível.")
    print("---------------------------------------------")

def imprimir_historico_recursivo(lista_pedidos: List):
    if not lista_pedidos:
        return
    
    print(f" - {lista_pedidos[0]}")

    imprimir_historico_recursivo(lista_pedidos[1:])

def gerar_relatorio_historico(pedidos_atendidos: List):
    print("\n--- RELATÓRIO: HISTÓRICO DE PEDIDOS ATENDIDOS ---")
    if not pedidos_atendidos:
        print("Nenhum pedido foi atendido com sucesso.")
    else:
        imprimir_historico_recursivo(pedidos_atendidos)
    print("--------------------------------------------------")