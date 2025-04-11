from fpdf import FPDF

def generate_pdf_report(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"JASW Test Report for {data['url']}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Runtime: {data['runtime']} seconds", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Score: {data['score']}%", ln=True, align='L')
    pdf.ln(10)

    for step in data['status']:
        txt = f"{step['step']} - {step['result']}"
        if 'error' in step:
            txt += f" (Error: {step['error']})"
        pdf.multi_cell(0, 10, txt)

    pdf.output("results/report.pdf")
