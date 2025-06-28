# 🤖 AI-Powered Internal Chatbot for FinSolve Technologies

This project is a submission for the [Codebasics Resume Challenge](https://codebasics.io/challenge/codebasics-gen-ai-data-science-resume-project-challenge/), where the objective is to build an AI-powered internal chatbot with **role-based access control (RBAC)** and **Retrieval-Augmented Generation (RAG)** for enterprise-level data access.

---

## 📌 Problem Statement

FinSolve Technologies is a FinTech company facing delays in communication and siloed data access across departments like Finance, HR, Marketing, Engineering, and C-Level Executives. The goal is to build a secure, intelligent chatbot that:

- Authenticates users and assigns roles
- Retrieves department-specific data
- Responds to natural language queries with context-aware answers
- Maintains strict access control

---

## ✅ Features

- 🔐 **Role-Based Access Control (RBAC)**: Each user only accesses permitted data
- 💬 **Natural Language Query Handling** using Gemini/GPT
- 🧠 **RAG Architecture**: Embeds and retrieves relevant document chunks
- ⚡ **FastAPI Backend** with modular role endpoints
- 🖥️ **Streamlit Frontend**: Simple and intuitive UI
- 🗃️ **Chroma Vector Store** with Nomic embeddings

---

## 🧱 Tech Stack

| Component      | Tool/Library         |
|----------------|----------------------|
| Language       | Python               |
| Backend        | FastAPI              |
| Frontend       | Streamlit            |
| AI Engine      | Gemini / GPT         |
| Embeddings     | Nomic via Ollama     |
| Vector Store   | Chroma               |
| Authentication | Custom role mapping  |
| Environment    | .env for API keys    |

---

## 🗂️ Repository Structure

```
code-basics-gen-ai-resume-project/
│
├── app.py # Main FastAPI app
├── .env # Environment file for Gemini API key
├── README.md # Project documentation (you are here)
│
├── finance.py # Finance role backend logic
├── hr.py # HR role backend logic
├── marketing.py # Marketing role backend logic
├── engineering.py # Engineering role backend logic
├── c-level.py # C-Level Executive logic
├── general.py # General employee queries logic
│
├── text chunking and vectorization/
│ ├── [scripts for data loading]
│ └── [vector store creation logic using Chroma]
```

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/Kalyan9847/code-basics-gen-ai-resume-project.git
cd code-basics-gen-ai-resume-project
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Add your Gemini API Key:**

Create a .env file in the root directory:
```env
GEMINI_API_KEY=your-gemini-api-key-here
```

4. **Run Vectorization Scripts**

Make sure you run scripts inside text chunking and vectorization/ to build your vector database using ChromaDB.

5. **Start the FastAPI Server**

```bash
uvicorn app:app --reload
```

6. **Run the Streamlit App**

In another terminal:
```bash
streamlit run streamlit_app.py
```


## 🔐 Roles & Permissions

| Role        | Access Scope                                |
|-------------|----------------------------------------------|
| Finance     | Financial reports, reimbursements, budgets   |
| HR          | Payroll, attendance, employee records        |
| Marketing   | Campaign data, customer feedback             |
| Engineering | Tech documentation, development guidelines   |
| C-Level     | Full access to all organizational data       |
| General     | Company policies, FAQs, events               |


## 📊 Evaluation Criteria

This project is evaluated based on the following parameters (as per Codebasics Resume Challenge):

- ✅ **Functionality**: The chatbot should correctly handle user queries and deliver role-specific responses.
- ✅ **Code Quality**: Code should be clean, modular, well-structured, and properly commented.
- ✅ **Innovation**: Unique ideas in query processing, access control, or enhancements are rewarded.
- ✅ **Presentation**: Clear and professional explanation with a complete demo.
- ✅ **NLP Query Understanding**: The chatbot should understand natural language, provide contextual answers, and handle vague questions.
- ✅ **User Experience**: The chatbot UI should be intuitive, fast, and responsive.
- ✅ **Modularity**: Clear separation of concerns – UI, API, vector logic, and access control.
- ✅ **Documentation**: A well-documented README covering setup, roles, tech stack, and architecture.
- ✅ **Scalability & Extensibility**: Easily adaptable to additional roles, data sources, and new features.


## 🔗 License

This project was created for educational and portfolio purposes as part of the [Codebasics Resume Challenge](https://codebasics.io/challenge/codebasics-gen-ai-data-science-resume-project-challenge).  
All data used is fictional and intended for demonstration only.

Feel free to fork and build upon this work, but please give proper credit.  
🔒 This project is shared under the **MIT License**.

