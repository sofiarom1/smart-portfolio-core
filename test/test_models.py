# tests/test_models.py
import pytest
from src.modelos import Posicion, Instrumento
import pytest
from test.exceptions import PosicionNoExisteError

@pytest.mark.parametrize(
    "precio_entrada, precio_actual, cantidad, esperado",
    [
        (100, 150, 10, 500),
        (200, 180, 5, -100),
        (50, 50, 7, 0),
    ],
)
def test_calculo_pnl(
    precio_entrada,
    precio_actual,
    cantidad,
    esperado,
    instrumento_test,
):
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=cantidad,
        precio_entrada=precio_entrada,
    )

    pnl = posicion.calcular_ganancia_no_realizada(
        precio_actual=precio_actual
    )

    assert pnl == pytest.approx(esperado)

def test_remover_activo_inexistente_lanza_error(portafolio_vacio):
    with pytest.raises(PosicionNoExisteError):
        portafolio_vacio.remover_posicion(ticker="NFLX")


# Tests para Portafolio
def test_agregar_posicion_incrementa_lista(portafolio_vacio, instrumento_test):
    """Verifica que agregar una posición aumenta la lista del portafolio."""
    from src.modelos import Posicion
    
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=10,
        precio_entrada=100
    )
    
    assert len(portafolio_vacio.posiciones) == 0
    
    portafolio_vacio.agregar_posicion(posicion)
    
    assert len(portafolio_vacio.posiciones) == 1
    assert portafolio_vacio.posiciones[0] == posicion


def test_agregar_multiple_posiciones(portafolio_vacio, instrumento_test):
    """Verifica que se pueden agregar múltiples posiciones."""
    from src.modelos import Posicion
    
    posicion1 = Posicion(
        instrumento=instrumento_test,
        cantidad=10,
        precio_entrada=100
    )
    
    instrumento2 = Instrumento(ticker="AAPL", tipo="Accion", sector="tecnologia")
    posicion2 = Posicion(
        instrumento=instrumento2,
        cantidad=5,
        precio_entrada=200
    )
    
    portafolio_vacio.agregar_posicion(posicion1)
    portafolio_vacio.agregar_posicion(posicion2)
    
    assert len(portafolio_vacio.posiciones) == 2


def test_remover_posicion_existente(portafolio_vacio, instrumento_test):
    """Verifica que se puede remover una posición existente."""
    from src.modelos import Posicion
    
    posicion = Posicion(
        instrumento=instrumento_test,
        cantidad=10,
        precio_entrada=100
    )
    
    portafolio_vacio.agregar_posicion(posicion)
    assert len(portafolio_vacio.posiciones) == 1
    
    portafolio_vacio.remover_posicion(ticker="TSLA")
    assert len(portafolio_vacio.posiciones) == 0

