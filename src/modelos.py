from dataclasses import dataclass

@dataclass(frozen=True)
class Instrumento:
    ticker: str
    tipo: str    
    sector: str
    