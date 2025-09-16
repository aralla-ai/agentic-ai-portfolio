class RiskAgent:
    def __init__(self, sharpe_min=1.0, max_dd=-0.25, vol_max=0.3):
        self.sharpe_min = sharpe_min
        self.max_dd = max_dd
        self.vol_max = vol_max

    def assess(self, metrics: dict):
        notes = []
        decision = "PASS"

        if metrics["Sharpe"] < self.sharpe_min:
            notes.append(f"Sharpe too low ({metrics['Sharpe']:.2f} < {self.sharpe_min})")
            decision = "FAIL"

        if metrics["MaxDD"] < self.max_dd:
            notes.append(f"Drawdown too high ({metrics['MaxDD']:.2%} < {self.max_dd:.0%})")
            decision = "FAIL"

        if metrics["Volatility"] > self.vol_max:
            notes.append(f"Volatility too high ({metrics['Volatility']:.2%} > {self.vol_max:.0%})")
            decision = "FAIL"

        if not notes:
            notes.append("All risk checks passed")

        return {"Decision": decision, "Notes": notes}