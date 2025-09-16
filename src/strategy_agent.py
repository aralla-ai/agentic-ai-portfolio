import pandas as pd
import numpy as np

class StrategyAgent:
    def __init__(self, data):
        self.data = data.copy()

    def sma_crossover(self, fast=10, slow=50):
        df = self.data.copy()
        df[f"SMA_{fast}"] = df["Close"].rolling(fast).mean()
        df[f"SMA_{slow}"] = df["Close"].rolling(slow).mean()
        df["Signal"] = 0
        df.loc[df[f"SMA_{fast}"] > df[f"SMA_{slow}"], "Signal"] = 1
        df.loc[df[f"SMA_{fast}"] < df[f"SMA_{slow}"], "Signal"] = -1
        df["Position"] = df["Signal"].shift(1).fillna(0)
        df["Return"] = df["Close"].pct_change()
        df["Strategy_Return"] = df["Position"] * df["Return"]
        return df

    def rsi_strategy(self, lower=30, upper=70):
        df = self.data.copy()
        df["Signal"] = 0
        df.loc[df["RSI_14"] < lower, "Signal"] = 1
        df.loc[df["RSI_14"] > upper, "Signal"] = -1
        df["Position"] = df["Signal"].shift(1).fillna(0)
        df["Return"] = df["Close"].pct_change()
        df["Strategy_Return"] = df["Position"] * df["Return"]
        return df

    def bollinger_breakout(self):
        df = self.data.copy()
        df["Signal"] = 0
        df.loc[df["Close"] > df["BB_UPPER"], "Signal"] = 1
        df.loc[df["Close"] < df["BB_LOWER"], "Signal"] = -1
        df["Position"] = df["Signal"].shift(1).fillna(0)
        df["Return"] = df["Close"].pct_change()
        df["Strategy_Return"] = df["Position"] * df["Return"]
        return df
