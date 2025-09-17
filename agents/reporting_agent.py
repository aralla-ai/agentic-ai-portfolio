import os
from fpdf import FPDF

class ReportingAgent:
    def __init__(self, output_dir="../reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf(self, eval_result, filename="report.pdf"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Portfolio Evaluation Report", ln=True, align="C")

        # Portfolio Metrics
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "Portfolio Metrics:", ln=True)
        pdf.set_font("Arial", size=10)
        for k, v in eval_result["Portfolio"].items():
            pdf.cell(200, 8, f"{k}: {v:.4f}", ln=True)

        # Benchmarks
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "Benchmark Metrics:", ln=True)
        pdf.set_font("Arial", size=10)
        for bench, metrics in eval_result["Benchmarks"].items():
            pdf.cell(200, 8, f"{bench}:", ln=True)
            for k, v in metrics.items():
                pdf.cell(200, 8, f"   {k}: {v:.4f}", ln=True)

        # Past Average
        pdf.ln(5)
        pdf.cell(200, 10, f"Average Past Sharpe: {eval_result['Avg_Past_Sharpe']:.4f}", ln=True)

        # Decision
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"Decision: {eval_result['Decision']}", ln=True)

        # Save
        out_path = os.path.join(self.output_dir, filename)
        pdf.output(out_path)
        return out_path
