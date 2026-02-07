from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_processing import FileProcessingService

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF file, save it, and extract its text.
    """
    if not file.filename.endswith(".pdf"):
         raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # 1. Save the file
    file_path = await FileProcessingService.save_file(file)
    
    # 2. Extract text
    extracted_text = FileProcessingService.extract_text(file_path)
    
    return {
        "filename": file.filename, 
        "file_path": str(file_path),
        "character_count": len(extracted_text),
        "preview": extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
    }
