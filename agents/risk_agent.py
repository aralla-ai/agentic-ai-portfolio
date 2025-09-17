import numpy as np

class RiskAgent:
    def __init__(self, sharpe_min=1.0, vol_max=0.3, dd_max=-0.25):
        self.sharpe_min = sharpe_min
        self.vol_max = vol_max
        self.dd_max = dd_max

    def compute_metrics(self, returns):
        # Default metrics structure
        metrics = {"Sharpe": 0, "Volatility": 0, "CAGR": 0, "MaxDD": 0}

        if returns is None or len(returns.dropna()) == 0:
            return metrics

        strat_curve = (1 + returns.fillna(0)).cumprod()
        years = (returns.index[-1] - returns.index[0]).days / 365.25 if len(returns) > 1 else 1

        metrics["CAGR"] = strat_curve.iloc[-1]**(1/years) - 1 if years > 0 else 0
        metrics["Volatility"] = returns.std() * np.sqrt(252)
        metrics["Sharpe"] = (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        roll_max = strat_curve.cummax()
        metrics["MaxDD"] = (strat_curve / roll_max - 1).min()

        return metrics

    def evaluate(self, returns):
        metrics = self.compute_metrics(returns)

        # Default PASS
        decision = "PASS"
        if metrics["Sharpe"] < self.sharpe_min:
            decision = "FAIL"
        if metrics["Volatility"] > self.vol_max:
            decision = "FAIL"
        if metrics["MaxDD"] < self.dd_max:
            decision = "FAIL"

        # Flatten: merge metrics + decision
        metrics["Decision"] = decision
        return metrics
