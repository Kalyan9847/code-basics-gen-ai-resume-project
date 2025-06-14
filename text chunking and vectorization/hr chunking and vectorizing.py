import pandas as pd
import json
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

df = pd.read_csv("C:/Users/madda/Desktop/LLM/Resume Challenge/RAG Based Chatbot for FinTech Company/hr/hr_data.csv")

def row_to_sentence_full(row):
    return (
        f"{row['full_name']} (Employee ID: {row['employee_id']}) is a {row['role']} in the {row['department']} department, "
        f"location: {row['location']}. They joined FinTechCo on {pd.to_datetime(row['date_of_joining']).strftime('%B %d, %Y')} "
        f"and were born on {pd.to_datetime(row['date_of_birth']).strftime('%B %d, %Y')}. Their email is {row['email']}, and their "
        f"manager is identified by Employee ID {row['manager_id']}. They earn an annual salary of ₹{row['salary']:,.2f}. "

        f"As of the last performance review on {pd.to_datetime(row['last_review_date']).strftime('%B %d, %Y')}, "
        f"they hold a performance rating of {row['performance_rating']}. Their attendance rate stands at {row['attendance_pct']}%, "
        f"with {row['leaves_taken']} leaves taken and {row['leave_balance']} days of leave remaining."
    )

df["summary"] = df.apply(row_to_sentence_full, axis=1)

# print(df['summary'].tolist()[:2])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    separators=["\n\n", "\n", " ", ""]
)

csv_text = "\n\n".join(df['summary'].tolist())

chunks = text_splitter.split_text(csv_text)
# print(chunks[:2])  # Print first two chunks for verification

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="hr_vector_store"
)

# Save the vectorstore to disk
vectorstore.persist()

# Load the vectorstore from disk
vectorstore = Chroma(
    persist_directory="hr_vector_store",
    embedding_function=embeddings
)   


query = input("Enter your query: ")
results = vectorstore.similarity_search(query, k=5)
for i, result in enumerate(results):
    print(f"Result {i+1}:\n{result.page_content}\n{'-'*40}")

# This code splits a document into chunks, embeds them, and stores them in a vector store for similarity search.
# It uses Langchain's text splitter, embeddings, and vector store functionalities.

