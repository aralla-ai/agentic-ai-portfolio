import pandas as pd
import numpy as np

class EvaluationAgent:
    def __init__(self, benchmark_agent, memory):
        self.benchmark_agent = benchmark_agent
        self.memory = memory

    def compute_metrics(self, returns):
        strat_curve = (1 + returns.fillna(0)).cumprod()
        years = (returns.index[-1] - returns.index[0]).days / 365.25
        cagr = strat_curve.iloc[-1]**(1/years) - 1 if years > 0 else 0
        vol = returns.std() * np.sqrt(252)
        sharpe = (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        roll_max = strat_curve.cummax()
        dd = (strat_curve / roll_max - 1).min()
        return {"CAGR": cagr, "Volatility": vol, "Sharpe": sharpe, "MaxDD": dd}

    def evaluate(self, portfolio_df):
        # Current portfolio
        portfolio_metrics = self.compute_metrics(portfolio_df["Portfolio_Return"])

        # Benchmarks
        benchmarks = self.benchmark_agent.evaluate()

        # Historical averages from memory
        history_df = pd.DataFrame(self.memory.history)
        if not history_df.empty and "Metrics" in history_df.columns:
            past_sharpes = [m["Sharpe"] for m in history_df["Metrics"] if m is not None and "Sharpe" in m]
            avg_past_sharpe = np.mean(past_sharpes) if past_sharpes else 0
        else:
            avg_past_sharpe = 0

        # Decision: adopt if Sharpe > both benchmark Sharpe and past average
        best_benchmark_sharpe = max(m["Sharpe"] for m in benchmarks.values())
        decision = "ADOPT" if portfolio_metrics["Sharpe"] > best_benchmark_sharpe and portfolio_metrics["Sharpe"] > avg_past_sharpe else "REJECT"

        return {
            "Portfolio": portfolio_metrics,
            "Benchmarks": benchmarks,
            "Avg_Past_Sharpe": avg_past_sharpe,
            "Decision": decision
        }
