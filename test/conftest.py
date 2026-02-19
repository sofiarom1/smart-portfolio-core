# tests/conftest.py
import pytest
from src.modelos import Instrumento
from src.portafolio import Portafolio

@pytest.fixture
def instrumento_test():
    return Instrumento(ticker="TSLA", tipo="Tesla", sector= "tecnologia")

@pytest.fixture
def portafolio_vacio():
    return Portafolio()