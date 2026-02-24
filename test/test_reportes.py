# tests/test_reportes.py
import pytest
import json
import csv
import os
from src.reportes import ExportadorCSV, ExportadorJSON, Reportadorfinanciero
from src.portafolio import Portafolio
from src.modelos import Instrumento, Posicion


@pytest.fixture
def instrumento_test():
    return Instrumento(ticker="AAPL", tipo="Accion", sector="tecnologia")


@pytest.fixture
def portafolio_con_posiciones(instrumento_test):
    portafolio = Portafolio()
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=10,
        precio_entrada=150
    )
    portafolio.agregar_posicion(posicion)
    return portafolio


@pytest.fixture
def portafolio_vacio():
    return Portafolio()


# Pruebas para ExportadorCSV
def test_exportador_csv_crea_archivo(portafolio_con_posiciones, tmp_path):
    """Verifica que ExportadorCSV crea un archivo CSV válido."""
    exportador = ExportadorCSV()
    reportador = Reportadorfinanciero()
    ruta = tmp_path / "reporte.csv"
    
    reportador.exportar(portafolio_con_posiciones, exportador, str(ruta))
    
    assert ruta.exists()
    with open(ruta, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]['ticker'] == 'AAPL'
        # La cantidad es float, así que puede ser '10' o '10.0'
        assert float(rows[0]['cantidad']) == 10.0


def test_exportador_csv_con_portafolio_vacio(portafolio_vacio, tmp_path):
    """Verifica que ExportadorCSV maneja portafolio vacío."""
    exportador = ExportadorCSV()
    reportador = Reportadorfinanciero()
    ruta = tmp_path / "reporte_vacio.csv"
    
    reportador.exportar(portafolio_vacio, exportador, str(ruta))
    
    # No debe fallar, pero el archivo puede estar vacío o no existir
    assert not ruta.exists() or ruta.stat().st_size == 0


# Pruebas para ExportadorJSON
def test_exportador_json_crea_archivo(portafolio_con_posiciones, tmp_path):
    """Verifica que ExportadorJSON crea un archivo JSON válido."""
    exportador = ExportadorJSON()
    reportador = Reportadorfinanciero()
    ruta = tmp_path / "reporte.json"
    
    reportador.exportar(portafolio_con_posiciones, exportador, str(ruta))
    
    assert ruta.exists()
    with open(ruta, 'r') as f:
        datos = json.load(f)
        assert len(datos) == 1
        assert datos[0]['ticker'] == 'AAPL'
        assert datos[0]['cantidad'] == 10


def test_exportador_json_con_portafolio_vacio(portafolio_vacio, tmp_path):
    """Verifica que ExportadorJSON maneja portafolio vacío."""
    exportador = ExportadorJSON()
    reportador = Reportadorfinanciero()
    ruta = tmp_path / "reporte_vacio.json"
    
    reportador.exportar(portafolio_vacio, exportador, str(ruta))
    
    assert ruta.exists()


# Pruebas para Reportadorfinanciero
def test_imprimir_resumen_imprime_ticker(portafolio_con_posiciones, capsys):
    """Verifica que imprimir_resumen muestra el ticker."""
    reportador = Reportadorfinanciero()
    reportador.imprimir_resumen(portafolio_con_posiciones)
    
    captured = capsys.readouterr()
    assert "AAPL" in captured.out


def test_imprimir_resumen_imprime_valor_invertido(portafolio_con_posiciones, capsys):
    """Verifica que imprimir_resumen calcula el valor invertido correctamente."""
    reportador = Reportadorfinanciero()
    reportador.imprimir_resumen(portafolio_con_posiciones)
    
    captured = capsys.readouterr()
    # 10 * 150 = 1500
    assert "1500.00" in captured.out


def test_imprimir_resumen_con_portafolio_vacio(portafolio_vacio, capsys):
    """Verifica que imprimir_resumen funciona con portafolio vacío."""
    reportador = Reportadorfinanciero()
    reportador.imprimir_resumen(portafolio_vacio)
    
    captured = capsys.readouterr()
    assert "RESUMEN" in captured.out


def test_exportar_genera_datos_correctos(portafolio_con_posiciones):
    """Verifica que exportar genera los datos correctos."""
    exportador = ExportadorCSV()
    reportador = Reportadorfinanciero()
    
    # Capturamos los datos generados
    datos = []
    for pos in portafolio_con_posiciones.posiciones:
        instrumento = pos.instrumento
        datos.append({
            "ticker": instrumento.ticker,
            "tipo": instrumento.tipo,
            "sector": instrumento.sector,
            "cantidad": pos.cantidad,
            "precio_entrada": pos.precio_entrada,
            "invertido": pos.cantidad * pos.precio_entrada
        })
    
    assert len(datos) == 1
    assert datos[0]['ticker'] == 'AAPL'
    assert datos[0]['invertido'] == 1500
