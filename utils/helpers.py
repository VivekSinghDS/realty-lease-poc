import os 
import json
from typing import Any
import fitz  # PyMuPDF
import base64
from fastapi import UploadFile

from adapters.llms._openai import _OpenAI
from adapters.llms._perplexity import _Perplexity
from adapters.llms.base import LargeLanguageModel

def pdf_to_base64_images(pdf_asset: UploadFile) -> list[str]:
    """
    Takes a PDF file from a FastAPI UploadFile object, converts each page
    into a Base64 encoded PNG image, and returns a list of these strings.

    Args:
        pdf_asset: The UploadFile object containing the PDF.

    Returns:
        A list of strings, where each string is a Base64 encoded image.
    """
    base64_images = []
    
    # Read the content of the PDF file into an in-memory byte stream.
    pdf_bytes = pdf_asset.file.read()

    try:
        # Open the PDF document from the bytes.
        with fitz.open("pdf", pdf_bytes) as doc:
            for page_number in range(doc.page_count):
                page: Any = doc.load_page(page_number)
                
                # Render the page as a Pixmap (a raster image).
                # The 'dpi' parameter can be adjusted for higher or lower resolution.
                pix = page.get_pixmap(dpi=150)
                
                # Convert the Pixmap to a PNG image in an in-memory buffer.
                image_buffer = pix.tobytes(output="png")
                
                # Encode the image bytes to a Base64 string.
                base64_string = base64.b64encode(image_buffer).decode('utf-8')
                
                base64_images.append(base64_string)

        return base64_images

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []
    
def get_llm_adapter() -> LargeLanguageModel:
    llm_details = json.loads(str(os.environ.get('LLM')))
    if llm_details['provider'] == "openai":
        return _OpenAI()
    else:
        return _Perplexity()