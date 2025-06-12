from Estrutura.pilha import Pilha
from Models.engradado import Engradado
from typing import List, Tuple, Dict

# matriz 8x5
# cada coluna tem que ser uma nova instancia independente (pilha)

class Estoque:
    def __init__(self, linhas: int = 8, colunas: int = 5):
        self.linhas = linhas
        self.colunas = colunas
        
        # atributo
        self.layout: List[List[Pilha]] = []
        for _ in range(linhas):
            linha = []
            for _ in range(colunas):
                linha.append(Pilha())
            self.layout.append(linha)

        # dicionario de mapeamento: Dicionario: chave é a lista o tipo STR (Produto (ref.))
        # Tuple é a linha por coluna do tipo int
        self.mapa_produtos: Dict[str, List[Tuple[int, int]]] = {}

    def adicionar_engradado(self, engradado: Engradado) -> bool:
        codigo_produto = engradado.produto.codigo
        
        if codigo_produto in self.mapa_produtos: # se tiver pilha existente com espaço
            for linha, coluna in self.mapa_produtos[codigo_produto]:
                pilha = self.layout[linha][coluna]
                if not pilha.esta_cheia():
                    pilha.empilhar(engradado)
                    print(f"Engradado de '{engradado.produto.nome}' adicionado na posição ({linha}, {coluna}).")
                    return True

        # para pilhas vazias
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                pilha = self.layout[linha][coluna]
                if pilha.esta_vazia():
                    pilha.empilhar(engradado)
                    # adc a nova localização ao mapa de produtos
                    if codigo_produto not in self.mapa_produtos:
                        self.mapa_produtos[codigo_produto] = []
                    self.mapa_produtos[codigo_produto].append((linha, coluna))
                    print(f"Engradado de '{engradado.produto.nome}' adicionado em uma nova pilha na posição ({linha}, {coluna}).")
                    return True
        
        # se não conseguir adicionar:
        print(f"ERRO: Estoque cheio! Não foi possível adicionar o engradado de '{engradado.produto.nome}'.")
        return False

    def remover_engradado(self, codigo_produto: str) -> Engradado | None:
        if codigo_produto not in self.mapa_produtos or not self.mapa_produtos[codigo_produto]:
            print(f"ERRO: Produto com código '{codigo_produto}' não encontrado no estoque.")
            return None
            
        linha, coluna = self.mapa_produtos[codigo_produto][-1]
        pilha = self.layout[linha][coluna]

        if not pilha.esta_vazia():
            engradado_removido = pilha.desempilhar()
            print(f"Engradado de '{codigo_produto}' removido da posição ({linha}, {coluna}).")
            if pilha.esta_vazia():
                self.mapa_produtos[codigo_produto].remove((linha, coluna))
                print(f"AVISO: A pilha na posição ({linha}, {coluna}) ficou vazia e agora está disponível para qualquer produto.")

            return engradado_removido
        
        # Este trecho se torna menos provável de acontecer com a nova lógica, mas é bom manter.
        print(f"AVISO: Produto '{codigo_produto}' existe, mas não há engradados disponíveis.")
        return None

    def visualizar_estoque(self):
        """
        Imprime uma representação visual do layout do estoque.
        """
        print("\n" + "="*45)
        print(" " * 15 + "VISUALIZAÇÃO DO ESTOQUE")
        print("="*45)
        
        for linha in range(self.linhas):
            linha_str = f"Linha {linha} | "
            for coluna in range(self.colunas):
                pilha = self.layout[linha][coluna]
                if pilha.esta_vazia():
                    rep_pilha = "[  Vazio  ]"
                else:
                    produto_topo = pilha.ver_topo().produto.codigo
                    ocupacao = f"[{len(pilha)}/{pilha.capacidade}]"
                    rep_pilha = f"{produto_topo.ljust(6)} {ocupacao}"
                linha_str += rep_pilha + " | "
            print(linha_str)
            print("-" * (len(linha_str) - 2))
        print("="*45 + "\n")
    # Adicione este método dentro da classe Estoque em Core/estoque.py

    def consultar_produto(self, codigo_produto: str):
        if codigo_produto not in self.mapa_produtos or not self.mapa_produtos[codigo_produto]:
            print(f"Produto '{codigo_produto}' não encontrado no estoque.")
            return

        locais = self.mapa_produtos[codigo_produto]
        print(f"--- Consulta de Produto: '{codigo_produto}' ---")
        print(f"Encontrado em {len(locais)} pilha(s), nas posições: {locais}")
        
        total_itens = 0
        for linha, coluna in locais:
            pilha = self.layout[linha][coluna]
            total_itens += len(pilha) * pilha.ver_topo().quantidade_maxima

        print(f"Quantidade total de itens (aproximada): {total_itens}")
        print("------------------------------------------")

    #  converte o objeto Estoque inteiro para um dicionario
    def to_dict(self):
        return {
            "linhas": self.linhas,
            "colunas": self.colunas,
            # Converte cada pilha no layout para um dicionário
            "layout": [[pilha.to_dict() for pilha in linha] for linha in self.layout],
            "mapa_produtos": self.mapa_produtos
        }