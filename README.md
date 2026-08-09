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
## 📄 License & Copyright

> ⚠️ **IMPORTANT COPYRIGHT NOTICE**
> 
> **All Rights Reserved © 2026 T A Srinivas.**
> This repository is strictly for portfolio viewing purposes. **DO NOT COPY, CLONE, OR REDISTRIBUTE** this code. Stolen copies or unauthorized forks will be reported immediately for a GitHub copyright takedown.

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### 🌐 Let’s Connect

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)  
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)
- [![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=website&logoColor=white)](https://srinivasta.github.io)

