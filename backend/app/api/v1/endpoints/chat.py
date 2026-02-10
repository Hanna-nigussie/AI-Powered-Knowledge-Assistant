from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Ask a question about the uploaded documents.
    """
    # 1. Search for relevant context in the Vector DB
    results = rag_service.search(request.question, k=3)
    
    if not results:
        return ChatResponse(
            answer="I couldn't find any information in the uploaded documents to answer your question.",
            sources=[]
        )
    
    # 2. Prepare Context
    context_text = "\n\n".join([doc.page_content for doc in results])
    
    # 3. Call Gemini LLM
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from app.core.config import settings
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )
        
        prompt = f"""You are a helpful assistant. Use the following context to answer the user's question.
        If the answer is not in the context, say "I don't know based on the documents provided."
        
        Context:
        {context_text}
        
        Question: 
        {request.question}
        """
        
        response = llm.invoke(prompt)
        final_answer = response.content
        
    except Exception as e:
        final_answer = f"Error generating answer: {str(e)}"

    # 4. Format Sources
    sources = []
    for doc in results:
        sources.append(Source(content=doc.page_content, metadata=doc.metadata))
        
    return ChatResponse(answer=final_answer, sources=sources)
