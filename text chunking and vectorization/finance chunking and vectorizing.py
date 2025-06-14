# Create the vector database for finance documents
# ------------------------------------------------
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# # 1. Read and chunk both files
# def load_and_chunk(path, source_name):
#     with open(path, "r", encoding="utf-8") as f:
#         text = f.read()
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     chunks = splitter.split_text(text)
#     # Add metadata for source tracking
#     metadatas = [{"source": source_name} for _ in chunks]
#     return chunks, metadatas

# finance_files = [
#     ("finance/financial_summary.md", "financial_summary"),
#     ("finance/quarterly_financial_report.md", "quarterly_financial_report"),
# ]

# all_chunks = []
# all_metadatas = []

# for path, name in finance_files:
#     chunks, metadatas = load_and_chunk(path, name)
#     all_chunks.extend(chunks)
#     all_metadatas.extend(metadatas)

# # 2. Embed and store in a single vectorstore
# embeddings = OllamaEmbeddings(model="nomic-embed-text")
# vectorstore = Chroma.from_texts(
#     texts=all_chunks,
#     embedding=embeddings,
#     metadatas=all_metadatas,
#     persist_directory="finance_vector_store"
# )
# vectorstore.persist()
# print(f"Stored {len(all_chunks)} finance chunks in one vector database.")

# ------------------------------------------------------------------------------

# 3. Query the vectorstore

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Re-initialize the embedding model and vectorstore
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    persist_directory="finance_vector_store",
    embedding_function=embeddings
)

# Run a similarity search query
query = "What were the main revenue drivers this quarter?"
results = vectorstore.similarity_search(query, k=3)

# Display results
for i, doc in enumerate(results):
    print(f"--- Result {i+1} ---")
    print(f"Source: {doc.metadata['source']}")
    print(doc.page_content)
