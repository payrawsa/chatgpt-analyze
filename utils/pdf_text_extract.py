from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
import time
from typing import Optional, List
from concurrent.futures import ThreadPoolExecutor, TimeoutError

class PDFTextExtractor:
    def __init__(self):
        self.is_running = False

    def extract_text_from_pdf(self, pdf_path: str, max_pages: Optional[int] = None, start_page: int = 1, save_images: bool = False) -> List[str]:
        """
        Extract text from a PDF file using OCR.
        
        Args:
            pdf_path (str): Path to the PDF file
            max_pages (int, optional): Maximum number of pages to process. If None, processes all pages
            save_images (bool): Whether to save the intermediate images or clean them up
            
        Returns:
            List[str]: List of extracted text strings, one per page
        """
        if self.is_running:
            raise RuntimeError("Please wait for the previous extraction to finish.")

        self.is_running = True
        try:
            print(f"Extracting text from PDF: {pdf_path}")
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
                
            extracted_text = []
            temp_image_paths = []
            BATCH_SIZE = 10
            
            try:
                # Get first page to determine total pages if we don't have max_pages
                if max_pages is None:
                    with ThreadPoolExecutor() as executor:
                        future = executor.submit(convert_from_path, pdf_path, 
                                              first_page=1, 
                                              last_page=1,
                                              dpi=200, fmt='png')
                        first_page = future.result(timeout=10)
                        if not first_page:
                            raise Exception("Could not read the PDF file")
                        total_pages = len(first_page)
                else:
                    total_pages = max_pages+start_page-1
                print(f"Processing until page {total_pages} in batches of {BATCH_SIZE}")
                # Process pages in batches, starting from start_page
                for batch_start in range(start_page, total_pages + 1, BATCH_SIZE):
                    end_page = min(batch_start + BATCH_SIZE - 1, total_pages)
                    print(f"Processing batch: pages {batch_start} to {end_page}")
                    
                    # Convert batch of pages with timeout
                    with ThreadPoolExecutor() as executor:
                        future = executor.submit(convert_from_path, pdf_path, 
                                              first_page=batch_start, 
                                              last_page=end_page,
                                              dpi=200, fmt='png')
                        page_images = future.result(timeout=30)  # 30 second timeout per batch
                        if not page_images:
                            print(f"No images generated for pages {batch_start}-{end_page}")
                            continue
                            
                        # Process each page in the batch
                        for i, image in enumerate(page_images):
                            page_num = batch_start + i  # Calculate actual page number
                            # Save temporary image
                            temp_image_path = f"output/temp_page_{page_num}.png"
                            print(f"Saving temporary image: {temp_image_path}")
                            image.save(temp_image_path)
                            temp_image_paths.append(temp_image_path)
                            
                            # Extract text using OCR with Arabic language
                            text = pytesseract.image_to_string(image, lang='ara', config='--psm 3')
                            print(f"Extracted text from page {page_num}")
                            extracted_text.append(text)
                            
                            # Clean up the temporary image immediately if not saving
                            if not save_images and os.path.exists(temp_image_path):
                                try:
                                    os.remove(temp_image_path)
                                    temp_image_paths.remove(temp_image_path)
                                except Exception as e:
                                    print(f"Error cleaning up temporary file {temp_image_path}: {str(e)}")
                
            except TimeoutError as te:
                print(f"Timeout error: {str(te)}")
                raise Exception("PDF processing timed out. The file might be too large or corrupt.")
            except Exception as e:
                print(f"Error processing PDF: {str(e)}")
                raise

            finally:
                # Clean up temporary images if not saving
                if not save_images:
                    for temp_path in temp_image_paths:
                        if os.path.exists(temp_path):
                            try:
                                os.remove(temp_path)
                            except Exception as e:
                                print(f"Error cleaning up temporary file {temp_path}: {str(e)}")
            
            return extracted_text

        finally:
            self.is_running = False
            
    def get_text_from_pdf(self, pdf_path: str, max_pages: Optional[int] = None, start_page: int = 1) -> str:
        """
        Convenience method to get all text from PDF as a single string.
        
        Args:
            pdf_path (str): Path to the PDF file
            max_pages (int, optional): Maximum number of pages to process
            start_page (int): The page to start processing from
            
        Returns:
            str: Concatenated text from all processed pages
        """
        text_list = self.extract_text_from_pdf(pdf_path, max_pages, start_page=start_page)
        return "\n\n".join(text_list)
