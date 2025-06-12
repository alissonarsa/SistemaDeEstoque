from Estrutura.fila import Fila
from Core.estoque import Estoque
from Models.pedido import Pedido
from typing import List

def processar_pedidos(fila_pedidos: Fila, estoque: Estoque, pedidos_atendidos: List[Pedido]):
    print("\n" + "="*50)
    print("INICIANDO PROCESSAMENTO DA FILA DE PEDIDOS...")
    print("="*50)

    if fila_pedidos.esta_vazia():
        print("Fila de pedidos está vazia. Nada a processar.")
        print("="*50)
        return

    pedidos_a_processar = list(fila_pedidos.itens)
    for pedido_atual in pedidos_a_processar:
        fila_pedidos.desenfileirar() # remove o pedido da fila original
        print(f"\n[PROCESSANDO] {pedido_atual}")
        
        pedido_com_sucesso = True
        itens_removidos_nesta_rodada = [] # guarda os engradados caso o pedido falhe

        for item_pedido in pedido_atual.itens_pedido:
            print(f"  - Verificando item: {item_pedido.quantidade}x '{item_pedido.codigo_produto}'")
            
            quantidade_necessaria = item_pedido.quantidade
            quantidade_atendida = 0
            
            while quantidade_atendida < quantidade_necessaria:
                engradado_removido = estoque.remover_engradado(item_pedido.codigo_produto)
                
                if engradado_removido:
                    quantidade_atendida += engradado_removido.quantidade_maxima 
                    itens_removidos_nesta_rodada.append(engradado_removido)
                else:
                    print(f"  [ERRO] Estoque insuficiente para o produto '{item_pedido.codigo_produto}'. Pedido não pode ser atendido.")
                    print("  [AVISO] Revertendo remoções do estoque para este pedido.")
                    for engradado in itens_removidos_nesta_rodada:
                        estoque.adicionar_engradado(engradado)
                    
                    pedido_com_sucesso = False
                    fila_pedidos.enfileirar(pedido_atual) 
                    break 
            
            if not pedido_com_sucesso:
                break
        
        if pedido_com_sucesso:
            pedidos_atendidos.append(pedido_atual)
            print(f"[SUCESSO] Pedido de '{pedido_atual.nome_solicitante}' atendido e registrado.")

    print("\n" + "="*50)
    print("PROCESSAMENTO CONCLUÍDO.")
    print("="*50)