from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from google.genai import Client, types
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = Client(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Initialize Finance vector store
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    persist_directory="finance_vector_store",
    embedding_function=embeddings
)

# Define the request schema
class QueryRequest(BaseModel):
    query: str

# Define the endpoint
@app.post("/finance/query")
def ask_finance_ai(request: QueryRequest):
    user_query = request.query
    results = vectorstore.similarity_search(user_query, k=5)

    context_segments = [
        f"Result {i+1}: {doc.page_content}\n{'-'*80}\n"
        for i, doc in enumerate(results)
    ]
    context = "\n".join(context_segments)

    chat = client.chats.create(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=f"""
                You are an intelligent AI assistant. Answer the user's question only from the provided context.
                If the information is not found, say 'The document does not contain that detail.'
                Context: {context}
            """
        )
    )

    response = chat.send_message(user_query)
    return {"response": response.text}


