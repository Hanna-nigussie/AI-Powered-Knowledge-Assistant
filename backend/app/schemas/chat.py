from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    question: str

class Source(BaseModel):
    content: str
    metadata: dict

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
