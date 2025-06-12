import datetime

class Produto:

    # construtor:

    def __init__(self, codigo: str, lote: str, nome: str, peso: float, 
                 data_validade: str, data_fabricacao: str, 
                 preco_compra: float, preco_venda: float, 
                 fornecedor: str, fabricante: str, categoria: str):
        
        self.codigo = codigo # self é uma referencia ao objeto manipulado
        self.lote = lote
        self.nome = nome
        self.peso = peso
        # conversão de data string para parametro tipo data
        # data recebida em ano-mes-dia
        self.data_validade = datetime.datetime.strptime(data_validade, '%Y-%m-%d').date()
        self.data_fabricacao = datetime.datetime.strptime(data_fabricacao, '%Y-%m-%d').date()
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.fornecedor = fornecedor
        self.fabricante = fabricante
        self.categoria = categoria

    # metodo para representar o produto com as principais atribuições

    def __repr__(self):
        return f"Produto(Código: '{self.codigo}', Nome: '{self.nome}', Lote: '{self.lote}')"
    
    # converte o objeto Produto para um dicionário serializável
    def to_dict(self):
        return {
            "codigo": self.codigo,
            "lote": self.lote,
            "nome": self.nome,
            "peso": self.peso,
            # Converte as datas para string para salvar no JSON
            "data_validade": self.data_validade.isoformat(),
            "data_fabricacao": self.data_fabricacao.isoformat(),
            "preco_compra": self.preco_compra,
            "preco_venda": self.preco_venda,
            "fornecedor": self.fornecedor,
            "fabricante": self.fabricante,
            "categoria": self.categoria
        }