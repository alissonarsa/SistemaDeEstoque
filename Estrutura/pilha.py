from typing import Any, List # list de qualquer tipo

class Pilha:
    
    def __init__(self, capacidade: int = 5): # pilha iniciada com a capacidade maxima
        
        self.capacidade = capacidade
        self.itens: List[Any] = []  # A pilha será armazenada em uma lista Python.

    def esta_vazia(self) -> bool:
        return len(self.itens) == 0

    def esta_cheia(self) -> bool:
        return len(self.itens) == self.capacidade

    def empilhar(self, item: Any) -> bool:
        if not self.esta_cheia():
            self.itens.append(item)
            return True
        print(f"ERRO: A pilha está cheia! Não é possível empilhar o item {item}.")
        return False

    def desempilhar(self) -> Any:
        if not self.esta_vazia():
            return self.itens.pop() # remove o ultimo/topo!
        print("ERRO: A pilha está vazia! Não é possível desempilhar.")
        return None

    def ver_topo(self) -> Any:
        if not self.esta_vazia():
            return self.itens[-1]
        return None
    
    # metodos

    # contar
    def __len__(self):
        return len(self.itens)

    # demonstra como esta a pilha
    def __repr__(self) -> str:
        if self.esta_vazia():
            return "Pilha Vazia"
        
        # saida da pilha
        rep = "--- TOPO ---\n"
        # Imprime na ordem inversa
        for item in reversed(self.itens):
            rep += f"  {item}\n"
        rep += "--- BASE ---"
        return rep
    
    # converte o objeto Pilha para um dicionario
    def to_dict(self):
        return {
            "capacidade": self.capacidade,
            "itens": [item.to_dict() for item in self.itens]
        }