from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from src.data_provider import MarketDataProvider


class MLModel(ABC):
    @abstractmethod
    def entrenar(self, datos: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def predecir(self, datos: pd.DataFrame) -> str:
        pass


# Implementación concreta de MLModel con regresión lineal
class ModeloRegresionLineal(MLModel):

    def __init__(self):
        self._modelo = LinearRegression()
        self._entrenado = False

    def entrenar(self, datos: pd.DataFrame) -> None:
        df = datos.reset_index()
        X = df.index.values.reshape(-1, 1)
        y = df["Close"].values
        self._modelo.fit(X, y)
        self._entrenado = True

    def predecir(self, datos: pd.DataFrame) -> str:
        if not self._entrenado:
            self.entrenar(datos)
        ultimo_indice = len(datos)
        precio_actual = float(datos["Close"].iloc[-1])
        precio_futuro = float(self._modelo.predict([[ultimo_indice + 7]])[0])
        tendencia = "📈 ALZA" if precio_futuro > precio_actual else "📉 BAJA"
        return f"Predicción 7 días: ${round(precio_futuro, 2)} ({tendencia})"


@dataclass
class Instrumento:
    ticker: str
    tipo: str
    sector: str
    data_provider: Optional[object] = None
    ml_model: Optional[MLModel] = None

    def entrenar_modelo(self) -> None:
        if self.data_provider is None or self.ml_model is None:
            raise ValueError("Faltan dependencias: data_provider y ml_model")
        datos = self.data_provider.obtener_historia(self.ticker)
        if datos.empty:
            raise ValueError(f"No hay datos históricos para {self.ticker}")
        self.ml_model.entrenar(datos)
        print("Entrenando modelo... OK")

    def predecir_tendencia(self) -> str:
        if self.data_provider is None or self.ml_model is None:
            raise ValueError("Faltan dependencias: data_provider y ml_model")
        datos = self.data_provider.obtener_historia(self.ticker)
        if datos.empty:
            raise ValueError(f"No hay datos recientes para {self.ticker}")
        return self.ml_model.predecir(datos)


@dataclass
class Posicion:
    instrumento: Instrumento
    cantidad: float
    precio_entrada: float
    alerta_riesgo: bool = field(default=False, init=False)

    def __post_init__(self):
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")

    def calcular_valor_actual(self, precio_mercado: float) -> float:
        return self.cantidad * precio_mercado

    def calcular_ganancia_no_realizada(self, precio_actual: float) -> float:
        return (precio_actual - self.precio_entrada) * self.cantidad

    def evaluar_riesgo(self, precio_actual: float) -> bool:
        perdida = (self.precio_entrada - precio_actual) / self.precio_entrada
        self.alerta_riesgo = perdida > 0.10
        return self.alerta_riesgo
