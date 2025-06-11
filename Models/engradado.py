from .produto import Produto

class Engradado:
    
    def __init__(self, produto: Produto, quantidade_maxima: int): # produto é do tipo produto
        
        # atributos
        self.produto = produto
        self.quantidade_maxima = quantidade_maxima
        self.quantidade_atual = 0  # Todo engradado começa vazio

    def esta_cheio(self) -> bool: # tipo de retorno 
        return self.quantidade_atual == self.quantidade_maxima

    def esta_vazio(self) -> bool:
        return self.quantidade_atual == 0
    
    # meu produto é determinado pelo nome do engradado ent só somamos quantidade
    def adicionar_item(self) -> bool:

        if not self.esta_cheio():
            self.quantidade_atual += 1 # nome vem da variavel do produto
            print(f"""Item '{self.produto.nome}' adicionado. 
                  Quantidade atual: {self.quantidade_atual}/{self.quantidade_maxima}""")
            return True
        else:
            print(f"ERRO: Engradado de '{self.produto.nome}' já está cheio!")
            return False

    def remover_item(self) -> bool:

        if not self.esta_vazio():
            self.quantidade_atual -= 1
            print(f"""Item '{self.produto.nome}' removido.
                  Quantidade atual: {self.quantidade_atual}/{self.quantidade_maxima}""")
            return True
        else:
            print(f"ERRO: Engradado de '{self.produto.nome}' já está vazio!")
            return False
    
    # metodo representar o engradado

    def __repr__(self):
        return (f"Engradado(Produto: '{self.produto.nome}', "
                f"Ocupação: {self.quantidade_atual}/{self.quantidade_maxima})")