from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


with open("C:/Users/madda/Desktop/LLM/Resume Challenge/RAG Based Chatbot for FinTech Company/general/employee_handbook.md", "rb") as file:
    byte_data = file.read()

try:
    doc_text = byte_data.decode("utf-8")
except UnicodeDecodeError:
    doc_text = byte_data.decode("latin1") 

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

chunks = text_splitter.split_text(doc_text)
# print(chunks[:2])  # Print first two chunks for verification

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="general_vector_store"
)

# Save the vectorstore to disk
vectorstore.persist()

# Load the vectorstore from disk
vectorstore = Chroma(
    persist_directory="general_vector_store",
    embedding_function=embeddings
)   


query = input("Enter your query: ")
results = vectorstore.similarity_search(query, k=5)
for i, result in enumerate(results):
    print(f"Result {i+1}:\n{result.page_content}\n{'-'*40}")

# This code splits a document into chunks, embeds them, and stores them in a vector store for similarity search.
# It uses Langchain's text splitter, embeddings, and vector store functionalities.
