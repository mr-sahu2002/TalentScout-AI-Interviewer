import PyPDF2
import os

class PDFTextExtractor:
    """
    A simple class to extract text from PDF files.
    """
    
    def __init__(self, pdf_path: str):
        """
        Initialize the PDFTextExtractor with a PDF file path.
        
        Args:
            pdf_path (str): Path to the PDF file
        """
        self.pdf_path = pdf_path
        self._validate_file()
        
    def _validate_file(self) -> None:
        """Validate that the PDF file exists and is accessible."""
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found at: {self.pdf_path}")
        if not self.pdf_path.lower().endswith('.pdf'):
            raise ValueError("File must be a PDF document")
            
    def extract_text(self) -> str:
        """
        Extract text from the entire PDF.
        
        Returns:
            str: Concatenated text from all pages
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                    
                return text.strip()
                
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    def get_pdf_info(self) -> dict:
        """
        Get basic information about the PDF file.
        
        Returns:
            dict: Dictionary containing PDF metadata
        """
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                info = {
                    'number_of_pages': len(reader.pages),
                    'metadata': reader.metadata
                }
                return info
                
        except Exception as e:
            raise Exception(f"Error getting PDF information: {str(e)}")

if __name__ == "__main__":
    pdf_path = "pdf_name.pdf"
    extractor = PDFTextExtractor(pdf_path)

    # Get PDF info
    info = extractor.get_pdf_info()
    print(f"Your PDF has {info['number_of_pages']} page(s)")

    # Extract all text
    text = extractor.extract_text()
    print(text)
    print(type(text))