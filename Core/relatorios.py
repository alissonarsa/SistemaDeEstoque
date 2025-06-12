import datetime
from Core.estoque import Estoque
from typing import List

# --- Relatório 1: Produtos Próximos ao Vencimento ---

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