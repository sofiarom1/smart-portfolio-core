# Bono
from abc import ABC, abstractmethod
import csv
import json
from src.portafolio import Portafolio

# CONTRATO (OCP)

class Exportador(ABC):
    @abstractmethod
    def guardar(self, datos: list[dict], ruta: str) -> None:
        pass



# CSV

class ExportadorCSV(Exportador):
    def guardar(self, datos: list[dict], ruta: str) -> None:
        if not datos:
            return

        columnas = datos[0].keys()

        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(datos)


# JSON

class ExportadorJSON(Exportador):
    def guardar(self, datos: list[dict], ruta: str) -> None:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
from src.portafolio import Portafolio
from src.modelos import Posicion, Instrumento


class Reportadorfinanciero:
    """
    Esta clase no guarda cambios. Solo recibe un portafolio y genera salidad
    """
    def imprimir_resumen(self, portafolio):
        print("               RESUMEN DEL PORTAFOLIO               ")
        print(f"Tipo de Clase de Intrumento:",{})
        print(
            f"{'Ticker':<8} {'Tipo':<12} {'Sector':<12} "
            f"{'Cantidad':>10} {'P. entrada':>12} {'Invertido':>12}"
        )
        print("-" * 70)

        valor_total_invertido = 0.0

        for posicion in portafolio.posiciones:
            instrumento: Instrumento = posicion.instrumento
            invertido = posicion.cantidad * posicion.precio_entrada
            valor_total_invertido += invertido

            print(
                f"{instrumento.ticker:<8} "
                f"{instrumento.tipo:<12} "
                f"{instrumento.sector:<12} "
                f"{posicion.cantidad:>10.2f} "
                f"{posicion.precio_entrada:>12.2f} "
                f"{invertido:>12.2f}"
            )

        print("-" * 70)
        print(f"{'Valor total invertido:':<44}{valor_total_invertido:>26.2f}")
        print("=" * 70)

    def exportar(
        self,
        portafolio: Portafolio,
        exportador: Exportador,
        ruta: str
    ) -> None:

        datos = []

        for pos in portafolio.posiciones:
            instrumento = pos.instrumento

            datos.append({
                "ticker": instrumento.ticker,
                "tipo": instrumento.tipo,
                "sector": instrumento.sector,
                "cantidad": pos.cantidad,
                "precio_entrada": pos.precio_entrada,
                "invertido": pos.cantidad * pos.precio_entrada
            })

        exportador.guardar(datos, ruta)

