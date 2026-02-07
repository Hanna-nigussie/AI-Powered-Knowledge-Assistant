import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from pypdf import PdfReader

UPLOAD_DIR = Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True)

class FileProcessingService:
    @staticmethod
    async def save_file(file: UploadFile) -> Path:
        """
        Saves the uploaded file to the local disk.
        """
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path

    @staticmethod
    def extract_text(file_path: Path) -> str:
        """
        Extracts text from a PDF file using pypdf.
        """
        try:
            reader = PdfReader(str(file_path))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
