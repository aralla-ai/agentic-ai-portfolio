import pandas as pd
import numpy as np

class StrategyAgent:
    def __init__(self, data):
        self.data = data.copy()

    def sma_strategy(self, short=20, long=50):
        df = self.data.copy()
        df["SMA_Short"] = df["Close"].rolling(window=short, min_periods=short).mean()
        df["SMA_Long"] = df["Close"].rolling(window=long, min_periods=long).mean()
        df["Signal"] = np.where(df["SMA_Short"] > df["SMA_Long"], 1, -1)
        df["Strategy_Return"] = df["Signal"].shift(1) * df["Return"]
        return df.dropna()

    def rsi_strategy(self, period=14, lower=30, upper=70):
        df = self.data.copy()
        delta = df["Close"].diff()

        # Gains and losses
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=period, min_periods=period).mean()
        avg_loss = loss.rolling(window=period, min_periods=period).mean()

        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        df["Signal"] = 0
        df.loc[df["RSI"] < lower, "Signal"] = 1
        df.loc[df["RSI"] > upper, "Signal"] = -1

        df["Strategy_Return"] = df["Signal"].shift(1) * df["Return"]
        return df.dropna()

    def bollinger_strategy(self, window=20, num_std=2):
        df = self.data.copy()

        # Calculate Bollinger Bands
        df["MA"] = df["Close"].rolling(window=window, min_periods=window).mean()
        df["STD"] = df["Close"].rolling(window=window, min_periods=window).std()
        df["Upper"] = df["MA"] + num_std * df["STD"]
        df["Lower"] = df["MA"] - num_std * df["STD"]

        # Drop rows with NaNs
        df = df.dropna().copy()

        # Flatten arrays → guaranteed 1D alignment
        close = df["Close"].to_numpy().ravel()
        upper = df["Upper"].to_numpy().ravel()
        lower = df["Lower"].to_numpy().ravel()

        signals = np.zeros(len(df))
        signals[close < lower] = 1    # Buy
        signals[close > upper] = -1   # Sell

        df["Signal"] = signals
        df["Strategy_Return"] = df["Signal"].shift(1) * df["Return"]

        return df



    def generate(self):
        results = {}
        results["SMA"] = self.sma_strategy()
        results["RSI"] = self.rsi_strategy()
        results["Bollinger"] = self.bollinger_strategy()
        return results
