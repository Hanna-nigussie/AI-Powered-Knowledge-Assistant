from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Define where to save the vector database locally
PERSIST_DIRECTORY = "./chroma_db"

class RAGService:
    def __init__(self):
        # 1. Initialize Embeddings (runs locally on CPU)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 2. Initialize Vector Store (ChromaDB)
        self.vector_store = Chroma(
            collection_name="documents",
            embedding_function=self.embeddings,
            persist_directory=PERSIST_DIRECTORY
        )
        
        # 3. Initialize Text Splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )

    def add_document(self, text: str, source: str):
        """
        Splits text into chunks and saves them to the Vector DB.
        """
        # Create unique chunks from the text
        docs = self.text_splitter.create_documents(
            [text], 
            metadatas=[{"source": source}]
        )
        
        # Add to ChromaDB (automatically persists)
        self.vector_store.add_documents(docs)
        return len(docs)

    def search(self, query: str, k: int = 3):
        """
        Searches for the most relevant document chunks.
        """
        return self.vector_store.similarity_search(query, k=k)

# Create a singleton instance
rag_service = RAGService()
