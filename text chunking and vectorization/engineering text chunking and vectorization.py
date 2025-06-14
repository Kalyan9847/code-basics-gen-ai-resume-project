from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma



with open("C:/Users/madda/Desktop/LLM/Resume Challenge/RAG Based Chatbot for FinTech Company/engineering/engineering_master_doc.md", "r") as file:
    doc_text = file.read()

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
    persist_directory="engineering_vector_store"
)

# Save the vectorstore to disk
vectorstore.persist()

# Load the vectorstore from disk
vectorstore = Chroma(
    persist_directory="engineering_vector_store",
    embedding_function=embeddings
)   


query = "Fintech company and overview"
results = vectorstore.similarity_search(query, k=2)
for i, result in enumerate(results):
    print(f"Result {i+1}:\n{result.page_content}\n{'-'*40}")

# This code splits a document into chunks, embeds them, and stores them in a vector store for similarity search.
# It uses Langchain's text splitter, embeddings, and vector store functionalities.



# # Initialize ChromaDB client
# chroma_client = chromadb.HttpClient(host='localhost', port=8000)

# # Create a collection
# collection = chroma_client.get_collection(name='engineering_fintech')

# Insert data into the collection
# collection.add(
#     documents= chunks,
#     embeddings=embeddings.embed_documents(chunks),
#     ids=[f"chunk_{i}" for i in range(len(chunks))]
# )   



# results = collection.query(
#     query_embeddings=[query_vector],
#     n_results=5
# )

# # Print top results
# with open('results.txt', 'a') as file:
#     for i, doc in enumerate(results['documents'][0]):
#         # print(f"Result {i+1}: {doc}\n{'-'*80}")
#             file.write(f"Result {i+1}: {doc}\n{'-'*80}\n")
# print("Results saved to results.txt")
