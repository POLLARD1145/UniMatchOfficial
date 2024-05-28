import fitz  # PyMuPDF
from docx import Document

def pdf_to_docx(pdf_path, docx_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Create a new Word document
    doc = Document()
    
    # Extract text from each page and add it to the Word document
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        doc.add_paragraph(text)
    
    # Save the Word document
    doc.save(docx_path)
    
    # Close the PDF file
    pdf_document.close()

# Usage example
file_path = 'E:\\Third Year\\CS 301 - Project Management\\School project\\UniMatchOfficial\\Django\\UniMatch\\ai_logic\\pdfdocs\\LIST-OF-REGISTERED-AND-ACCREDITED-QUALIFICATIONS-ON-THE-ZQF-AUGUST-20237520.pdf'

pdf_to_docx(file_path, "output.docx")