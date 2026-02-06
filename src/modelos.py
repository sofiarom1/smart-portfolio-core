from dataclasses import dataclass

@dataclass(frozen=True)
class Instrumento:
    ticker: str
    tipo: str    
    sector: str
    
class Posicion:
    def __init__(self, instrumento:Instrumento, cantidad: float, precio_entrada: float):
        self.instrumento: Instrumento
        self.cantidad:float
        self.precio_entrada: float 

@property
def cantidad(self) -> float:
        return self._cantidad
@cantidad.setter
def cantidad(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("La cantidad NO puede ser negativa")
        self._cantidad = value

def calcular_valor_actual(self, precio_mercado: float) -> float:
        return self.cantidad * float(precio_mercado)