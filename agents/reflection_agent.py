class ReflectionAgent:
    def __init__(self):
        pass

    def reflect(self, assessment: dict):
        notes = assessment["Notes"]
        reasoning = []
        new_params = {}

        for note in notes:
            if "Sharpe too low" in note:
                reasoning.append("Sharpe ratio too low -> increase slow SMA window for more stability.")
                new_params["sma_slow"] = 100
            if "Volatility too high" in note:
                reasoning.append("Volatility too high -> widen RSI thresholds to reduce over-trading.")
                new_params["rsi_lower"] = 25
                new_params["rsi_upper"] = 75
            if "Drawdown too high" in note:
                reasoning.append("Drawdown exceeded limit -> shift Allocator to equal-weight instead of Sharpe-weight.")
                new_params["allocation"] = "equal"

        if not reasoning:
            reasoning.append("All good - no changes needed.")

        return {"Reasoning": reasoning, "New_Params": new_params}
