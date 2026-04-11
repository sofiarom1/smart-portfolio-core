from abc import ABC, abstractmethod
import pandas as pd
import yfinance as yf



class MarketDataProvider(ABC):

    @abstractmethod
    def obtener_precio_actual(self, ticker: str) -> float:
        pass

    @abstractmethod
    def obtener_historia(
        self,
        ticker: str,
        dias: int = 365
    ) -> pd.DataFrame:
        pass



class YahooFinanceClient(MarketDataProvider):

    def obtener_precio_actual(self, ticker: str) -> float:
        try:
            t = yf.Ticker(ticker)
            return float(t.fast_info["last_price"])
        except Exception as e:
            raise ConnectionError(
                f"Error conectando a Yahoo Finance: {e}"
            )

    def obtener_historia(
        self,
        ticker: str,
        dias: int = 365
    ) -> pd.DataFrame:
        t = yf.Ticker(ticker)
        df = t.history(period="1y")
        return df
