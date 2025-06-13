import datetime
from Core import gerenciador_json
from Core.estoque import Estoque
from Core.processador import processar_pedidos
from Core.relatorios import gerar_relatorio_historico, gerar_relatorio_itens_em_falta, gerar_relatorio_vencimento
from Estrutura.fila import Fila
from Models.produto import Produto
from Models.engradado import Engradado
from Models.pedido import Pedido

def encontrar_produto_no_catalogo(catalogo, codigo):
    for p_dict in catalogo:
        if p_dict['codigo'] == codigo:
            return Produto(**p_dict)
    return None

def menu_produtos():
    """Exibe o menu de gerenciamento de produtos do catálogo."""
    while True:
        print("\n--- MENU DE PRODUTOS ---")
        print("1. Listar todos os produtos")
        print("2. Adicionar novo produto")
        print("3. Remover um produto")
        print("4. Alterar um produto")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            produtos = gerenciador_json.listar_produtos()
            if not produtos:
                print("Nenhum produto cadastrado no catálogo.")
            else:
                print("\n--- CATÁLOGO DE PRODUTOS ---")
                for p in produtos:
                    print(f"Código: {p['codigo']}, Nome: {p['nome']}, Preço Venda: R${p.get('preco_venda', 0):.2f}")
                print("----------------------------")

        elif opcao == "2":
            print("\n--- ADICIONAR NOVO PRODUTO ---")
            try:
                novo_produto = {
                    "codigo": input("Código: "), "lote": input("Lote: "), "nome": input("Nome: "),
                    "peso": float(input("Peso (kg): ")), "data_validade": input("Data de validade (AAAA-MM-DD): "),
                    "data_fabricacao": input("Data de fabricação (AAAA-MM-DD): "), "preco_compra": float(input("Preço de compra: R$")),
                    "preco_venda": float(input("Preço de venda: R$")), "fornecedor": input("Fornecedor: "),
                    "fabricante": input("Fabricante: "), "categoria": input("Categoria: ")
                }
                gerenciador_json.adicionar_produto(novo_produto)
                print("Produto adicionado com sucesso!")
            except ValueError:
                print("ERRO: Preço e peso devem ser números.")

        elif opcao == "3":
            codigo = input("Digite o código do produto que deseja remover: ")
            if gerenciador_json.remover_produto_por_codigo(codigo):
                print("Produto removido com sucesso!")
            else:
                print("ERRO: Produto não encontrado.")

        elif opcao == "4":
            codigo = input("Digite o código do produto para alterar: ")
            campo = input("Qual campo deseja alterar? (ex: nome, preco_venda): ").lower()
            novo_valor = input(f"Digite o novo valor para '{campo}': ")
            try:
                if campo in ["peso", "preco_compra", "preco_venda"]:
                    novo_valor = float(novo_valor)
                if gerenciador_json.alterar_produto(codigo, {campo: novo_valor}):
                    print("Produto alterado com sucesso!")
                else:
                    print("ERRO: Produto não encontrado.")
            except ValueError:
                print("ERRO: Valor inválido para o campo numérico.")

        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_estoque(estoque: Estoque, catalogo_produtos: list):
    """Exibe o menu de gerenciamento do estoque."""
    while True:
        print("\n--- MENU DE ESTOQUE ---")
        print("1. Visualizar layout do estoque")
        print("2. Adicionar engradado ao estoque")
        print("3. Remover engradado do estoque")
        print("4. Consultar produto no estoque")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            estoque.visualizar_estoque()
        elif opcao == "2":
            print("\n--- ADICIONAR ENGRADADO ---")
            codigo = input("Digite o código do produto do engradado: ")
            produto_obj = encontrar_produto_no_catalogo(catalogo_produtos, codigo)
            if produto_obj:
                try:
                    capacidade = int(input(f"Qual a capacidade do engradado de '{produto_obj.nome}'? "))
                    novo_engradado = Engradado(produto_obj, capacidade)
                    if estoque.adicionar_engradado(novo_engradado):
                        print("Engradado adicionado com sucesso!")
                except ValueError:
                    print("ERRO: Capacidade deve ser um número inteiro.")
            else:
                print("ERRO: Produto não encontrado no catálogo.")
        elif opcao == "3":
            print("\n--- REMOVER ENGRADADO ---")
            codigo = input("Digite o código do produto a ser removido: ")
            engradado_removido = estoque.remover_engradado(codigo)
            if engradado_removido:
                print(f"Um engradado de '{engradado_removido.produto.nome}' foi removido com sucesso.")
        elif opcao == "4":
             print("\n--- CONSULTAR PRODUTO ---")
             codigo = input("Digite o código do produto a ser consultado: ")
             estoque.consultar_produto(codigo)
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_pedidos(fila: Fila, estoque: Estoque, historico: list, catalogo: list):
    while True:
        print("\n--- MENU DE PEDIDOS ---")
        print("1. Registrar novo pedido na fila")
        print("2. Visualizar fila de pedidos pendentes")
        print("3. Processar TODOS os pedidos da fila")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("\n--- REGISTRAR NOVO PEDIDO ---")
            solicitante = input("Nome do solicitante: ")
            pedido = Pedido(solicitante)
            while True:
                codigo = input("Digite o código do produto (ou 'fim' para terminar): ")
                if codigo.lower() == 'fim':
                    break
                produto_obj = encontrar_produto_no_catalogo(catalogo, codigo)
                if produto_obj:
                    try:
                        qtd = int(input(f"Quantidade de '{produto_obj.nome}': "))
                        pedido.adicionar_item(codigo, qtd)
                    except ValueError:
                        print("ERRO: Quantidade deve ser um número.")
                else:
                    print("ERRO: Produto não encontrado no catálogo.")
            if pedido.itens_pedido:
                fila.enfileirar(pedido)
                print("Pedido registrado na fila com sucesso!")
        elif opcao == "2":
            print("\n--- FILA DE PEDIDOS PENDENTES ---")
            if fila.esta_vazia():
                print("Não há pedidos na fila.")
            else:
                print(fila)
            print("---------------------------------")
        elif opcao == "3":
            processar_pedidos(fila, estoque, historico)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_relatorios(estoque: Estoque, historico_pedidos: list):
    """Exibe o menu para geração de relatórios."""
    while True:
        print("\n--- MENU DE RELATÓRIOS ---")
        print("1. Relatório de Produtos Próximos ao Vencimento")
        print("2. Relatório de Itens em Falta no Estoque")
        print("3. Histórico de Pedidos Atendidos")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerar_relatorio_vencimento(estoque)
        elif opcao == "2":
            gerar_relatorio_itens_em_falta(estoque)
        elif opcao == "3":
            gerar_relatorio_historico(historico_pedidos)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_principal():
    estoque, fila_de_pedidos, pedidos_atendidos = gerenciador_json.carregar_estado_sistema()
    catalogo_produtos = gerenciador_json.listar_produtos()
    
    print("\nBem-vindo ao Sistema de Gerenciamento de Estoque!")
    
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Gerenciar Catálogo de Produtos")
        print("2. Gerenciar Estoque")
        print("3. Gerenciar Pedidos")
        print("4. Gerar Relatórios")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_produtos()
            catalogo_produtos = gerenciador_json.listar_produtos()
        elif opcao == "2":
            menu_estoque(estoque, catalogo_produtos)
        elif opcao == "3":
            menu_pedidos(fila_de_pedidos, estoque, pedidos_atendidos, catalogo_produtos)
        elif opcao == "4":
            menu_relatorios(estoque, pedidos_atendidos)
        elif opcao == "0":
            gerenciador_json.salvar_estado_sistema(estoque, fila_de_pedidos, pedidos_atendidos)
            print("Estado do sistema salvo. Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# rodeee
if __name__ == "__main__":
    menu_principal()