import json
from src.data_provider import YahooFinanceClient
from src.modelos import Instrumento, Posicion, ModeloRegresionLineal
from src.portafolio import Portafolio
from src.reportes import Reportadorfinanciero

def main():
    print("--- 🔮 SMART PORTFOLIO ORACLE ---\n")

    # 1. Pedir ticker
    ticker = input("Ingrese Ticker: ").upper().strip()

    # 2. Obtener datos y predecir
    provider = YahooFinanceClient()
    modelo = ModeloRegresionLineal()
    instrumento = Instrumento(
        ticker=ticker,
        tipo="Acción",
        sector="N/A",
        data_provider=provider,
        ml_model=modelo
    )

    print("Obteniendo datos... OK")
    instrumento.entrenar_modelo()

    precio_actual = provider.obtener_precio_actual(ticker)
    prediccion = instrumento.predecir_tendencia()

    print(f"\n📊 {ticker}")
    print(f"Precio actual:    ${precio_actual}")
    print(f"{prediccion}")

    # 3. Preguntar compra
    compra = input("\n¿Comprar? (s/n): ").strip().lower()

    if compra == "s":
        cantidad = float(input("Cantidad: "))

        posicion = Posicion(
            instrumento=instrumento,
            cantidad=cantidad,
            precio_entrada=precio_actual
        )

        # Evaluar riesgo
        posicion.evaluar_riesgo(precio_actual)

        # Guardar en portafolio
        fondo = Portafolio()
        fondo.agregar_posicion(posicion)

        # Guardar JSON
        datos = {
            "ticker": ticker,
            "cantidad": cantidad,
            "precio_entrada": precio_actual,
            "prediccion": prediccion,
            "alerta_riesgo": posicion.alerta_riesgo
        }
        with open("portafolio.json", "w") as f:
            json.dump(datos, f, indent=4)

        print("\nGuardado en portafolio.json ✅")

        # Reporte en consola
        reportador = Reportadorfinanciero()
        reportador.imprimir_resumen(fondo)

    else:
        print("\nOperación cancelada.")


if __name__ == "__main__":
    main()
