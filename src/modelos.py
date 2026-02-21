from dataclasses import dataclass

@dataclass(frozen=True)
class Instrumento:
    ticker: str
    tipo: str    
    sector: str
    
class Posicion:
    def __init__(self, instrumento: Instrumento, cantidad: float, precio_entrada: float):
        self.instrumento = instrumento
        self.cantidad = cantidad
        self.precio_entrada = precio_entrada 

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

    def calcular_ganancia_no_realizada(self, precio_actual: float) -> float:
        """
        Calcula la ganancia o pérdida no realizada de la posición.
        
        Args:
            precio_actual: Precio actual del instrumento en el mercado.
            
        Returns:
            Ganancia (positiva) o pérdida (negativa) no realizada.
        """
        return (precio_actual - self.precio_entrada) * self.cantidad
