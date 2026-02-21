from typing import List
from src.modelos import Posicion
from test.exceptions import PosicionNoExisteError

class Portafolio:
    def __init__(self) -> None:
        self.posiciones: List[Posicion] = []

    def agregar_posicion(self, posicion: Posicion) -> None:
        self.posiciones.append(posicion)

    def remover_posicion(self, ticker: str) -> None:
        """
        Remueve una posición del portafolio por su ticker.
        
        Args:
            ticker: Ticker del instrumento a remover.
            
        Raises:
            PosicionNoExisteError: Si no existe una posición con el ticker proporcionado.
        """
        for posicion in self.posiciones:
            if posicion.instrumento.ticker == ticker:
                self.posiciones.remove(posicion)
                return
        raise PosicionNoExisteError(f"No existe posición con ticker '{ticker}' en el portafolio.")