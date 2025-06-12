import datetime
from typing import NamedTuple # garantir que o pedido seja imutavel

class ItemPedido(NamedTuple):
    codigo_produto: str
    quantidade: int

class Pedido:
    def __init__(self, nome_solicitante: str):
        self.itens_pedido: list[ItemPedido] = []
        self.data_solicitacao: datetime.date = datetime.date.today()
        self.nome_solicitante: str = nome_solicitante

    def adicionar_item(self, codigo_produto: str, quantidade: int):
        item = ItemPedido(codigo_produto=codigo_produto, quantidade=quantidade)
        self.itens_pedido.append(item)
        print(f"Item adicionado ao pedido de {self.nome_solicitante}: {quantidade}x '{codigo_produto}'")

    # metodos
    
    def __repr__(self) -> str:
        # data para o padrão brasileiro
        data_formatada = self.data_solicitacao.strftime('%d/%m/%Y')
        # Pega a lista de itens e formata para exibição
        itens_str = ', '.join([f"{item.quantidade}x '{item.codigo_produto}'" for item in self.itens_pedido])
        
        return (f"Pedido(Solicitante: '{self.nome_solicitante}', Data: {data_formatada}, Itens: [{itens_str}])")

    def to_dict(self):
        return {
            "nome_solicitante": self.nome_solicitante,
            "data_solicitacao": self.data_solicitacao.isoformat(),
            "itens_pedido": [item._asdict() for item in self.itens_pedido]
        }