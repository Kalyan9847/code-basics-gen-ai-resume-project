from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from google.generativeai import GenerativeModel # Corrected import for gemini-2.0-flash
from google.generativeai.types import GenerationConfig # Corrected import for GenerationConfig
from dotenv import load_dotenv
import os

load_dotenv()
# Note: GEMINI_API_KEY should be loaded from environment variables.
# If running locally, ensure it's set in your .env file or system environment.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize the FastAPI app
app = FastAPI()

# Re-initialize the embedding model and vectorstore
embeddings = OllamaEmbeddings(model="nomic-embed-text")

class QueryRequest(BaseModel):
    # This role field in the payload is still sent by the frontend,
    # but the actual role for vectorstore connection will come from the URL path.
    role: str
    query: str

def connect_vectorstore(role_key: str):
    """
    Connect to the Chroma vector store based on the given role key.
    The role_key should be a lowercase string corresponding to the department.
    """
    supported_roles = [
        "finance", "marketing", "hr", "engineering", "general"
    ]
    if role_key not in supported_roles:
        # Raise an HTTPException for a bad request if the role is not supported
        raise HTTPException(status_code=400, detail=f"Unsupported department role: {role_key}. Supported roles are: {', '.join(supported_roles)}")
    
    # Construct the path to the vector store directory
    persist_directory_path = f"{role_key}_vector_store"

    # Check if the vector store directory exists before trying to connect
    if not os.path.exists(persist_directory_path):
        raise HTTPException(status_code=404, detail=f"Vector store for department '{role_key}' not found at {persist_directory_path}.")

    return Chroma(
        persist_directory=persist_directory_path,
        embedding_function=embeddings
    )

# Initialize the Gemini client outside the endpoint function for efficiency
# Use GenerativeModel directly for chat interactions with gemini-2.0-flash
gemini_model = GenerativeModel("gemini-2.0-flash")


# Endpoint for C-Level specific queries with a sub-role in the path
@app.post("/c-level/{sub_role}/query")
async def ask_ai_c_level(
    request: QueryRequest,
    sub_role: str = Path(..., description="The specific department role for C-Level executives (e.g., 'finance', 'marketing')")
):
    """
    Handles AI queries for C-Level executives, routing to the appropriate
    department's vector store based on the `sub_role` in the URL path.
    """
    # Use the sub_role from the path parameter, convert to lowercase for consistency
    department_role = sub_role.strip().lower() 
    user_query = request.query

    try:
        vectorstore = connect_vectorstore(department_role)
    except HTTPException as e:
        return {"response": e.detail} # Return the error message from the HTTPException

    # Perform similarity search to get context
    results = vectorstore.similarity_search(user_query, k=3)

    context_segments = [
        f"Result {i+1}: {doc.page_content}\n{'-'*80}\n"
        for i, doc in enumerate(results)
    ]
    context = "\n".join(context_segments)

    # Use the initialized gemini_model for chat interactions
    chat = gemini_model.start_chat(
        history=[] # Start with empty history for each new request
    )

    # Send system instruction as the first message to guide the model's behavior
    chat.send_message(
        f"""
        You are an intelligent AI assistant. Answer the user's question only from the provided context.
        If the information is not found, say 'The document does not contain that detail.'
        Context: {context}
        """
    )
    
    # Send the user query
    response = chat.send_message(user_query, 
                                 generation_config=GenerationConfig(
                                     temperature=0.0 # Keep temperature low for factual responses
                                 ))
    
    return {"response": response.text}


# Endpoint for general department queries
@app.post("/{role}/query")
async def ask_ai_general(
    request: QueryRequest,
    role: str = Path(..., description="The department role (e.g., 'finance', 'general', 'hr')")
):
    """
    Handles AI queries for general department roles, routing to the appropriate
    department's vector store based on the `role` in the URL path.
    """
    # Use the role from the path parameter, convert to lowercase for consistency
    department_role = role.strip().lower()
    user_query = request.query

    try:
        vectorstore = connect_vectorstore(department_role)
    except HTTPException as e:
        return {"response": e.detail} # Return the error message from the HTTPException

    # Perform similarity search to get context
    results = vectorstore.similarity_search(user_query, k=3)

    context_segments = [
        f"Result {i+1}: {doc.page_content}\n{'-'*80}\n"
        for i, doc in enumerate(results)
    ]
    context = "\n".join(context_segments)

    # Use the initialized gemini_model for chat interactions
    chat = gemini_model.start_chat(
        history=[] # Start with empty history for each new request
    )

    # Send system instruction as the first message to guide the model's behavior
    chat.send_message(
        f"""
        You are an intelligent AI assistant. Answer the user's question only from the provided context.
        If the information is not found, say 'The document does not contain that detail.'
        Context: {context}
        """
    )
    
    # Send the user query
    response = chat.send_message(user_query,
                                 generation_config=GenerationConfig(
                                     temperature=0.0 # Keep temperature low for factual responses
                                 ))
    
    return {"response": response.text}


# Use this back-end server
