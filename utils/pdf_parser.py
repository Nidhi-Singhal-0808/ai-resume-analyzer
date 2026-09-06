import io
from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file object.
    Returns plain text string or raises an exception if unreadable.
    """
    try:
        # Read the uploaded file into bytes stream
        bytes_data = uploaded_file.read()
        pdf_file_obj = io.BytesIO(bytes_data)
        
        reader = PdfReader(pdf_file_obj)
        text = ""
        
        if len(reader.pages) == 0:
            raise ValueError("The uploaded PDF file contains no pages.")
            
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        if not text.strip():
            raise ValueError("Could not extract readable text. The PDF might be scanned/image-based.")
            
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {str(e)}")