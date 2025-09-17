import pandas as pd
import numpy as np
import yfinance as yf

class BenchmarkAgent:
    def __init__(self, tickers=["SPY"], start="2020-01-01", end=None):
        self.tickers = tickers
        self.start = start
        self.end = end
        self.data = {}

    def fetch(self):
        for ticker in self.tickers:
            df = yf.download(ticker, start=self.start, end=self.end, progress=False)
            df["Return"] = df["Close"].pct_change()
            self.data[ticker] = df
        return self.data

    def compute_metrics(self, returns):
        strat_curve = (1 + returns.fillna(0)).cumprod()
        years = (returns.index[-1] - returns.index[0]).days / 365.25
        cagr = strat_curve.iloc[-1]**(1/years) - 1 if years > 0 else 0
        vol = returns.std() * np.sqrt(252)
        sharpe = (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        roll_max = strat_curve.cummax()
        dd = (strat_curve / roll_max - 1).min()
        return {"CAGR": cagr, "Volatility": vol, "Sharpe": sharpe, "MaxDD": dd}

    def evaluate(self):
        metrics = {}
        for ticker, df in self.data.items():
            metrics[ticker] = self.compute_metrics(df["Return"])
        return metrics
