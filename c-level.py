# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import OllamaEmbeddings
# from google.genai import Client, types
# from dotenv import load_dotenv
# import os

# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# client = Client(api_key= GEMINI_API_KEY)

# # Re-initialize the embedding model and vectorstore
# embeddings = OllamaEmbeddings(model="nomic-embed-text")

# def connect_vectorstore(role: str):
#     """Connect to the Chroma vector store."""
#     return Chroma(
#         persist_directory=f"{role}_vector_store",
#         embedding_function=embeddings
#     )
# vectorstore = connect_vectorstore(input("Enter the role: ").strip().lower())

# # vectorstore = Chroma(
# #     persist_directory="hr_vector_store",
# #     embedding_function=embeddings
# # )

# # Run a similarity search query
# user_query = input("Enter your query: ")
# results = vectorstore.similarity_search(user_query, k=3)

# context_segments = []
# for i, doc in enumerate(results):
#     context_segments.append(f"Result {i+1}: {doc.page_content}\n{'-'*80}\n")

# context = "\n".join(context_segments)

# chat = client.chats.create(
#     model="gemini-2.0-flash",
#     config = types.GenerateContentConfig(
#             system_instruction=f"""
#                     You are an intelligent AI assistant. Answer the user's question only from the provided context.
#                     If the information is not found, say 'The document does not contain that detail.'
#                     Context: {context}""",

#     )
# )

# print("\n\nGemini Response:\n")
# response = chat.send_message(user_query)
# print(response.text)

# ----------------------------------------------------------------
from fastapi import FastAPI 
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from google.genai import Client, types
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = Client(api_key= GEMINI_API_KEY)

app = FastAPI()

# Re-initialize the embedding model and vectorstore
embeddings = OllamaEmbeddings(model="nomic-embed-text")

class QueryRequest(BaseModel):
    role: str
    query: str

def connect_vectorstore(role: str):
    """Connect to the Chroma vector store."""
    supported_roles = [
        "finance", "marketing", "hr", "engineering", "general"
    ]
    if role not in supported_roles:
        raise ValueError(f"Unsupported role: {role}")
    return Chroma(
        persist_directory=f"{role}_vector_store",
        embedding_function=embeddings
    )

@app.post("/query")
def ask_ai(request: QueryRequest):
    role = request.role.strip().lower()
    user_query = request.query

    try:
        vectorstore = connect_vectorstore(role)
    except ValueError as e:
        return {"error": str(e)}

    results = vectorstore.similarity_search(user_query, k=3)

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