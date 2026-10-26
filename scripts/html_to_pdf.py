import pdfkit
import os

html_path = "plugin_outputs/forensics_report.html"
pdf_path = "plugin_outputs/forensics_report.pdf"

# Update this path if wkhtmltopdf.exe is not in PATH
#wkhtmltopdf_path = r"C:\Users\User\Downloads\wkhtmltox-0.12.6-1.mxe-cross-win64\bin\wkhtmltopdf.exe"
# scripts/html_to_pdf.py
wkhtmltopdf_path = r"D:\MemoryForensicsTool\bin\wkhtmltopdf.exe"


# Check if HTML file exists
if not os.path.exists(html_path):
    print("❌ HTML report not found. Please generate it first.")
    exit()

# PDF options for better formatting
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None,
    'enable-local-file-access': '',  # Required to access local CSS
}

try:
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)
    print(f"[+] PDF generated: {pdf_path}")
except Exception as e:
    print(f"[!] Failed to generate PDF: {e}")
