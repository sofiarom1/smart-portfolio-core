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
        dias: int
    ) -> pd.DataFrame:
        pass


class YahooFinanceClient:

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

        # Simplificación: siempre 1 año
        df = t.history(period="1y")

        return df
list_tickers=['AAPL','TSLA','AMZN','GOOGL','META','NFLLX']

provider = YahooFinanceClient()

precio = provider.obtener_precio_actual("AAPL")
print("Precio actual:", precio)

hist = provider.obtener_historia("AAPL")
print(hist.head())