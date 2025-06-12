from Models.produto import Produto
from Models.engradado import Engradado
from Estrutura.pilha import Pilha
from Estrutura.fila import Fila
from Models.pedido import Pedido
from Core.estoque import Estoque
import json
import os
from Core import gerenciador_json

# --- Bloco Principal de Execução ---

# 1. Carregar o catálogo de produtos a partir do JSON
produtos_disponiveis = gerenciador_json.carregar_catalogo_produtos('catalogo_produtos.json')

if not produtos_disponiveis:
    print("Encerrando o programa por falta de catálogo de produtos.")
    exit()

# 2. Inicializar os componentes do sistema
meu_estoque = Estoque()
fila_de_pedidos = Fila()
pedidos_atendidos_com_sucesso = []

# 3. Popular o estoque usando os produtos carregados do catálogo
# Função auxiliar para encontrar um produto no catálogo pelo código
def encontrar_produto(codigo):
    for p in produtos_disponiveis:
        if p.codigo == codigo:
            return p
    return None

p_cola = encontrar_produto("REF001")
if p_cola:
    for _ in range(4):
        meu_estoque.adicionar_engradado(Engradado(p_cola, 24))

p_arroz = encontrar_produto("GRS005")
if p_arroz:
    for _ in range(2):
        meu_estoque.adicionar_engradado(Engradado(p_arroz, 50))

# O resto do arquivo continua igual...
print("--- ESTADO INICIAL DO ESTOQUE ---")
meu_estoque.visualizar_estoque()
# ... etc