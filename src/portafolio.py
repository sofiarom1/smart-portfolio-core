from typing import List
from src.modelos import Posicion

class Portafolio:
    def __init__(self) -> None:
        self.posiciones: List[Posicion] = []

    def agregar_posicion(self, posicion: Posicion) -> None:
        self.posiciones.append(posicion)