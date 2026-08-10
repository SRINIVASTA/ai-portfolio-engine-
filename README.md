# AI Portfolio Engine 🚀

A multi-user, multi-tenant hybrid SaaS platform built with a Node.js/Express backend API, a React frontend dashboard, and an integrated Python machine-learning/compilation pipeline. The platform automatically converts any developer's public GitHub profile into a stylized portfolio website, complete with an integrated Retrieval-Augmented Generation (RAG) chatbot trained on repository documentation and scoped strictly by user ID to prevent data leakage.

## 🏗️ System Architecture

```text
[ External Developer ] ---> Sign In with GitHub Handle (Passport.js OAuth)
                                    |
                                    v
                        [ Node.js/Express Server ] <---+ Triggers Child Process execution

                                    |                  |
            +-----------------------+------------------+----+

            |                                               |
            v                                               v
[ backend/routes/sync.js ]                         [ backend/compiler.py ]
- Scrapes repositories via API                     - Protocol-agnostic regex URL parser
- Extracts metrics & repository homepages          - Google AI-style sidebar live HTML crawler

            |                                               |
            |                                               v
            |                                      [ index.html Landing Page ]
            |                                      - Visual multi-track sorted component rows
            v                                               
[ backend/ml_processor.py ] 
- Processes text context chunking transformations
- Slices markdown into semantic embeddings
            |                                               
            +-----------------------+-----------------------+
                                    |
                                    v
                       [ Supabase PostgreSQL DB ]
               - Matrix Tables: 'users', 'repositories', 'documents'
               - Scoped Vector isolation filters (pgvector spatial models)
                                    |
                                    v
                     [ Interactive Frontend Shell ]
               - React Client Web Workspace (Home.jsx, ProfileShell.jsx)
               - Tenant-isolated RAG Chatbot Column (chat.js Node API router)
```

## 🛠️ Tech Stack & Architecture Matrix

| Layer | Component | Description |
| :--- | :--- | :--- |
| **API Web Server** | `Node.js / Express` | Orchestrates system lifecycles, user authentication, profile sync jobs, and backend routing endpoints. |
| **Authentication** | `Passport.js (OAuth)` | Handles secure developer sign-ins and registers active profile access tokens via GitHub. |
| **Database** | `PostgreSQL (Supabase)` | Manages multi-tenant relational configurations, tracking schema metrics and vector states (`pgvector`). |
| **AI Processing** | `Python (ml_processor.py)` | Manages text token isolation, high-dimensional data vector chunking, and semantic embedding pipelines. |
| **UI Code Compiler** | `Python (compiler.py)` | Runs high-fidelity scraping rules to build visual portfolio layouts split into thematic category rows. |
| **Frontend Shell** | `React (Vite / JSX)` | Serves the interactive user control panel, metric configurations, and client chatbot chat wrapper windows. |

## 📁 Repository Structure

```text
ai-portfolio-engine-/
├── .streamlit/
│   └── config.toml         # Streamlit server layout theme definitions configuration manual
├── backend/
│   ├── api/
│   │   ├── chat.js         # Node.js API controller managing chatbot chat routing traffic
│   │   └── config/
│   │       └── passport.js # Secure passport strategy framework tracking GitHub OAuth states
│   ├── models/
│   │   └── Schema.sql      # Primary database definition blueprints for PostgreSQL tables
│   ├── routes/
│   │   ├── auth.js         # Routing controllers managing developer session controls
│   │   └── sync.js         # API endpoint executing web scraper routines via python execution workers
│   ├── compiler.py         # Advanced multi-track layout engine featuring loose subdomain extraction rules
│   ├── ml_processor.py     # Matrix vector calculations script processing text document chunking blocks
│   └── server.js           # Core framework initialization file launching the backend Express runtime
├── frontend/src/pages/
│   ├── Home.jsx            # Dynamic React page loading application analytics and metrics
│   └── ProfileShell.jsx    # Component renderer displaying the generated developer index portfolio
├── app.py                  # Main Python script managing application SaaS entry configurations
├── index.html              # Compiled landing page layout containing dynamically sorted track rows
├── package.json            # Node.js backend system npm package dependency definitions manifest
├── requirements.txt        # Python pip library execution tracking requirements manifest
└── README.md               # Technical project documentation and system layout manual
```

## ⚙️ Compilation & Link Interception Engine Architecture

The core python compilation engine (`compiler.py`) uses a multi-tier, high-fidelity tracking sequence to securely build multi-tenant landing layers:

1. **Protocol-Agnostic Extraction:** Deep regular expression passes trace and extract embedded deployment signatures (`.streamlit.app`) out of raw texts even if they lack explicit protocol prefixes (e.g. `https://`).
2. **Google AI-Style Fallback Scraper:** If API data keys drop during transmission, the script launches an active HTTP crawler layer that fetches the raw HTML code of the repository webpage, parsing the code block layout to isolate the true live application link from the repository's **About Sidebar Box** layout automatically.
3. **Destructive Split Segregation Protection:** Link extraction steps run at the absolute apex of the loop, shielding custom random subdomain hashes from case-insensitive terminal string scrubbers (`git clone`, `pip install`, `streamlit run` stripping arrays).
4. **Dynamic Row-Track Categorization Grid:** Repositories automatically sort into independent, thematic layout rows (**Row 1: Generative AI Studios**, **Row 2: FinTech Engines**, **Row 3: Automation Utilities**) with automated self-hiding empty nodes.

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
Initialize dependencies for both runtime language platforms:
```bash
# Install backend Node.js packages
npm install

# Install verified Python dependencies
pip install -r requirements.txt
```

### 3. Launch the Application Servers
```bash
# Launch the backend Node API server framework
node backend/server.js

# Launch the Streamlit local testing environment
streamlit run app.py
```

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

- [![LinkedIn](https://shields.io)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://shields.io)](https://www.kaggle.com/srinivasta)  
- [![Email](https://shields.io)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://shields.io)](https://github.com/srinivasta)
- [![Website](https://shields.io)](https://srinivasta.github.io)
