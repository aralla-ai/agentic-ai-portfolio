import pandas as pd

class MemoryAgent:
    def __init__(self):
        self.history = []

    def record(self, strategy_name, metrics, assessment, reflection=None):
        entry = {
            "Strategy": strategy_name,
            "Metrics": metrics,
            "Decision": assessment["Decision"],
            "Notes": "; ".join(assessment["Notes"]),
            "Reflection": reflection["Reasoning"] if reflection else None,
            "Params": reflection["New_Params"] if reflection else None
        }
        self.history.append(entry)

    def analyze(self):
        df = pd.DataFrame(self.history)
        if df.empty:
            return "No history yet", []

        # Count failures by strategy
        fail_counts = df[df["Decision"] == "FAIL"]["Strategy"].value_counts()
        exclusions = fail_counts[fail_counts >= 2].index.tolist()

        summary = f"Strategies frequently failing: {', '.join(exclusions)}" if exclusions else "No exclusions needed."
        return summary, exclusions

    def export(self, path="../logs/Day17_memory_log.csv"):
        pd.DataFrame(self.history).to_csv(path, index=False)
