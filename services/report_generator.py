from fpdf import FPDF
import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "JASW - Test Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_section(self, title, content):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, content)
        self.ln(4)

def generate_pdf_report(result_data, output_path):
    pdf = PDFReport()
    pdf.add_page()

    pdf.add_section("Test URL", result_data.get("url", "N/A"))
    pdf.add_section("Test Status", result_data.get("status", "N/A"))
    pdf.add_section("Runtime", f"{result_data.get('runtime', 0):.2f} seconds")
    pdf.add_section("Score", f"{result_data.get('score', 0)}%")

    pdf.add_section("Summary", result_data.get("summary", "No summary provided."))

    if "steps" in result_data:
        step_text = ""
        for idx, step in enumerate(result_data["steps"], 1):
            status = step.get("status", "N/A")
            step_text += f"{idx}. {step.get('description', 'No description')} - [{status}]\n"
        pdf.add_section("Steps", step_text)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.add_section("Generated At", timestamp)

    pdf.output(output_path)
