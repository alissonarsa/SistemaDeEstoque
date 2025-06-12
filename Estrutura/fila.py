from collections import deque # bom para trabalhar com fila
from typing import Any

class Fila:
    
    def __init__(self):
        self.itens = deque() # inicia a fila

    def esta_vazia(self) -> bool:
        return not self.itens

    def enfileirar(self, item: Any):
        self.itens.append(item)

    def desenfileirar(self) -> Any:
        if not self.esta_vazia():
            return self.itens.popleft() # retira do inicio
        print("ERRO: A fila está vazia! Não é possível desenfileirar.")
        return None

    def ver_inicio(self) -> Any: # se tiver vazia: none
        if not self.esta_vazia():
            return self.itens[0]
        return None
    
    # metodos

    # contar
    def __len__(self) -> int:
        return len(self.itens)

    # demonstra a fila
    def __repr__(self) -> str:
        if self.esta_vazia():
            return "Fila Vazia"
        
        # Mostra a fila da frente para trás
        return f"Fila: [INÍCIO] {', '.join(str(item) for item in self.itens)} [FIM]"