import pandas as pd

class AllocatorAgent:
    def __init__(self, method="equal"):
        self.method = method

    def allocate(self, strategies: dict, metrics: dict, risk_assessments: dict):
        approved = {name: df for name, df in strategies.items()
                    if risk_assessments[name]["Decision"] == "PASS"}
        approved_metrics = {name: metrics[name] for name in approved.keys()}

        if not approved:
            return None, "No strategies passed risk checks"

        if self.method == "equal":
            weights = {name: 1/len(approved) for name in approved}
        elif self.method == "sharpe":
            sharpes = {name: m["Sharpe"] for name, m in approved_metrics.items()}
            total = sum(sharpes.values())
            weights = {name: s/total for name, s in sharpes.items()}

        portfolio = pd.DataFrame(index=list(approved.values())[0].index)
        for name, df in approved.items():
            portfolio[name] = df["Strategy_Return"] * weights[name]
        portfolio["Portfolio_Return"] = portfolio.sum(axis=1)
        portfolio["Cumulative"] = (1 + portfolio["Portfolio_Return"]).cumprod()

        return weights, portfolio
