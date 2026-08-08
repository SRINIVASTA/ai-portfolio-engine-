# AI Portfolio Engine 🚀

A multi-user, multi-tenant SaaS platform built in Python using Streamlit that automatically converts any developer's public GitHub profile into a sleek portfolio website. The platform features an integrated Retrieval-Augmented Generation (RAG) chatbot trained on repository documentation and scoped strictly by user ID to prevent data leakage.

## 🏗️ System Architecture

```text
[ External Developer ] ---> Sign In with GitHub Handle
                                    |
                                    v
                       [ Streamlit Core App Server ]
                                    |
            +-----------------------+-----------------------+

            |                                               |
            v                                               v
[ GitHub REST API Sync Worker ]                   [ AI Vector Processor Engine ]
- Scrapes profile repositories                   - Parses project README docs
- Extracts star & language metrics               - Slices text into semantic vectors

            |                                               |
            +-----------------------+-----------------------+
                                    |
                                    v
                       [ Supabase PostgreSQL DB ]
               - Matrix Tables: 'users', 'repositories'
               - Scoped Vector isolation filters (pgvector)
                                    |
                                    v
                     [ Interactive Frontend Shell ]
               - Left Column: Dynamic portfolio layout
               - Right Column: Tenant-isolated RAG Chatbot
```

## 🛠️ Tech Stack & Architecture

| Layer | Component | Description |
| :--- | :--- | :--- |
| **Frontend & Backend** | `Streamlit` | Orchestrates the web user interface framework and backend logic in pure Python. |
| **Data Scraping** | `GitHub REST API` | Pulls repository metrics, primary programming languages, and raw markdown contents. |
| **Database** | `PostgreSQL (Supabase)` | Manages user profiles, repository states, and deep vector spatial models (`pgvector`). |
| **AI Orchestration** | `RAG Engine` | Processes structural chunking transformations to feed localized data to the LLM. |

## 📁 Repository Structure

```text
ai-portfolio-engine/
├── .streamlit/
│   └── config.toml         # Custom application branding and layout parameters
├── app.py                  # Main architecture script managing SaaS entry and dashboard routines
├── requirements.txt        # Production environment pip dependency configuration manifest
└── README.md               # Technical project documentation and system layout manual
```

## 🔐 Multi-Tenant Security & Context Isolation

To ensure complete privacy and data security across multiple users, the platform applies a strict relational filter inside the document search queries:

```sql
-- Secure Stored Procedure query applied inside the vector search pipeline
SELECT * FROM documents 
WHERE user_id = current_portfolio_owner_id 
ORDER BY embedding <=> query_embedding 
LIMIT 5;
```
This relational database design ensures that User A's recruiter chatbot can **never** accidentally view, read, or process source code vectors belonging to User B's profile.

## 🚀 Getting Started Locally

### 1. Clone the Project
```bash
git clone https://github.com
cd ai-portfolio-engine-
```

### 2. Install Project Dependencies
Ensure you have Python 3.9+ installed, then install the verified dependencies:
```bash
pip install -r requirements.txt
```

### 3. Launch the Local Application Server
```bash
streamlit run app.py
```
The server will initialize locally and open your developer portal dashboard at `http://localhost:8501`.

## 📈 Future System Roadmap
- [ ] Connect a live LLM integration key (Google Gemini / Groq API) to generate conversational answers.
- [ ] Enable real high-dimensional vector uploads directly to a Supabase database instance.
- [ ] Set up custom subdomain tracking strings (`username.portfolio.dev`) for deployment mapping.

---
Developed with ❤️ by [T A Srinivas](https://github.io)
