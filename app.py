import streamlit as st 
import requests 

# Force strict dark mode styling layout
st.set_page_config(page_title="AI Portfolio Engine", layout="wide", initial_sidebar_state="collapsed") 

# Import specialized modular blocks from our file dependencies
from ml_processor import load_ml_classifier, run_dynamic_sync_pipeline
from chatbot_agent import handle_recruiter_chatbot

# 1. Initialize Global Application States 
if "logged_in" not in st.session_state: 
 st.session_state.logged_in = False 
if "username" not in st.session_state: 
 st.session_state.username = None 
if "chat_history" not in st.session_state: 
 st.session_state.chat_history = [] 
if "vault_context" not in st.session_state: 
 st.session_state.vault_context = "" 
if "niche_brand" not in st.session_state:
 st.session_state.niche_brand = "general"

# --- LANDING PAGE (SaaS Entry Point) --- 
if not st.session_state.logged_in: 
 st.title("🚀 Turn Your GitHub Into An AI Portfolio") 
 st.subheader("Deploy a self-updating website with an interactive recruiter chatbot trained on your code.") 
 st.write("---") 
 
 st.write("### Multi-User Gateway Authentication") 
 input_username = st.text_input("Enter GitHub Username or Profile Link:", placeholder="e.g., srinivasta or https://github.com") 
 
 if st.button("Sign In to Portfolio", type="primary"): 
  raw_input = input_username.strip() 
 
  # 🎯 BULLETPROOF PROFILE LINK CLEANER FOR RECRUITMENT SAAS PLATFORMS: 
  if "/" in raw_input: 
   cleaned_username = [piece for piece in raw_input.split("/") if piece][-1] 
  else: 
   cleaned_username = raw_input 
 
  cleaned_username = cleaned_username.replace("github.com", "").strip() 
 
  if cleaned_username: 
   st.session_state.logged_in = True 
   st.session_state.username = cleaned_username 
   st.session_state.vault_context = "" 
   st.session_state.chat_history = [] 
   st.session_state.niche_brand = "general"
   st.rerun() 
  else: 
   st.error("Please provide a valid developer username to proceed.") 

# --- PORTFOLIO DASHBOARD --- 
else: 
 username = st.session_state.username 
 
 # Dynamic Visual Theming Layer injected directly into the HTML root components
 if st.session_state.niche_brand == "capital_vantage":
  st.markdown("<style> :root { --primaryColor: #00D4B2; } .stButton>button { color: #00D4B2; border-color: #00D4B2; } </style>", unsafe_allow_html=True)
 elif st.session_state.niche_brand == "transition_control":
  st.markdown("<style> :root { --primaryColor: #FF5A5F; } .stButton>button { color: #FF5A5F; border-color: #FF5A5F; } </style>", unsafe_allow_html=True)
 
 col1, col2 = st.columns(2) 
 with col1: 
  if st.session_state.niche_brand == "capital_vantage":
   st.title("📈 💰 🚀 CapitalVantage: GenAI Financial Intelligence")
   st.write("`Autonomous Agent for Financial Auditing! 📊`")
  elif st.session_state.niche_brand == "transition_control":
   st.title("📈 📊 🚀 TransitionControl: AI-Driven BPO Intelligence")
   st.write("`Autonomous Command Center for Global Business Migrations! 🌐`")
  else:
   st.title(f"✨ Developer Portfolio: {username}") 
 with col2: 
  if st.button("Log Out of System", type="secondary", use_container_width=True): 
   st.session_state.logged_in = False 
   st.session_state.username = None 
   st.session_state.chat_history = [] 
   st.session_state.vault_context = "" 
   st.session_state.niche_brand = "general"
   st.rerun() 
 
 st.write("`✓ Verified Production Architecture Integration Enabled`") 
 st.write("---") 
 
 left_layout, right_chatbot = st.columns(2, gap="large") 
 
 with left_layout: 
  st.header("📁 Core Tracked Repositories") 
  if st.button("🔄 Sync Live GitHub Repositories Now", type="primary"): 
   run_dynamic_sync_pipeline(username)
  else: 
   st.info("Click the Sync button above to scrape public GitHub API records dynamically.") 
   
 with right_chatbot: 
  handle_recruiter_chatbot(username)
import os
import joblib
import requests
import streamlit as st
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

def chunk_text_data(text, max_chars=800): 
 if not text or not isinstance(text, str): 
  return [] 
 words = text.split() 
 chunks = [] 
 current_chunk = [] 
 for word in words: 
  current_chunk.append(word) 
  if len(" ".join(current_chunk)) >= max_chars: 
   chunks.append(" ".join(current_chunk)) 
   current_chunk = [] 
 if current_chunk: 
  chunks.append(" ".join(current_chunk)) 
 return chunks 

def self_train_and_bootstrap_model(repos):
    dataset_descriptions = []
    dataset_labels = []
    for repo in repos:
        desc = repo.get("description", "") or ""
        name = repo.get("name", "").lower()
        combined_text = f"{name}. {desc.lower()}"
        if not desc: continue
        
        assigned_label = "general_portfolio"
        if any(w in combined_text for w in ["invoice", "ledger", "tax", "banking", "finance", "capital", "vantage"]):
            assigned_label = "capital_vantage"
        elif any(w in combined_text for w in ["migration", "workflow", "governance", "risk", "bpo", "control", "roadmap"]):
            assigned_label = "transition_control"
            
        if assigned_label != "general_portfolio":
            dataset_descriptions.append(f"{repo['name']}. {desc}")
            dataset_labels.append(assigned_label)
            
    if len(set(dataset_labels)) > 1:
        auto_pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        auto_pipeline.fit(dataset_descriptions, dataset_labels)
        joblib.dump(auto_pipeline, "industry_classifier.pkl")
        return auto_pipeline
    return None

@st.cache_resource
def load_ml_classifier():
    if os.path.exists("industry_classifier.pkl"):
        return joblib.load("industry_classifier.pkl")
    return None

def run_dynamic_sync_pipeline(username):
   with st.spinner("Accessing GitHub REST endpoints..."): 
    try: 
     target_url = f"https://github.com{username}/repos?per_page=100" 
     headers = {"Accept": "application/vnd.github.v3+json"} 
     pat_token = st.secrets.get("GITHUB_PAT_TOKEN", None) 
     if pat_token: 
      headers["Authorization"] = f"token {pat_token}" 
 
     response = requests.get(target_url, headers=headers) 
     if response.status_code == 200: 
       repos = response.json() 
       if isinstance(repos, list): 
        st.success(f"Successfully tracked and parsed {len(repos)} public repositories!") 
        temp_context = [] 
        
        classifier_pipeline = load_ml_classifier()
        if not classifier_pipeline:
         classifier_pipeline = self_train_and_bootstrap_model(repos)
         
        fintech_weight, bpo_weight = 0, 0
        for repo in repos: 
         desc = repo.get('description', '') or ''
         text_context = f"{repo.get('name', '')}. {desc}"
         
         assigned_tag = "general"
         if classifier_pipeline and desc:
          predicted = classifier_pipeline.predict([text_context])[0]
          assigned_tag = predicted
          if predicted == "capital_vantage": fintech_weight += 1
          elif predicted == "transition_control": bpo_weight += 1
          
         with st.container(border=True): 
          if assigned_tag == "capital_vantage": st.subheader(f"📈 {repo['name']} [Fintech Asset]")
          elif assigned_tag == "transition_control": st.subheader(f"🛠️ {repo['name']} [BPO System]")
          else: st.subheader(repo['name']) 
           
          st.write(f"**Stars:** ⭐ {repo['stargazers_count']} | **Language:** 📝 {repo['language'] or 'Markdown'}")
          st.write(repo['description'] or "No public description provided.") 
          temp_context.append(f"Repository: {repo['name']}\nDescription: {repo['description'] or 'None'}\nLanguage: {repo['language'] or 'Unknown'}") 
 
          try: 
           default_branch = repo.get('default_branch', 'main') 
           readme_url = f"https://githubusercontent.com{username}/{repo['name']}/{default_branch}/README.md" 
           readme_req = requests.get(readme_url, headers=headers if pat_token else None) 
           if readme_req.status_code == 200 and len(readme_req.text.strip()) > 5: 
            text_slices = chunk_text_data(readme_req.text) 
            st.caption(f"🧠 RAG Engine: Split readme into {len(text_slices)} context vectors.") 
            temp_context.append(f"README Content Slices for {repo['name']}:\n{readme_req.text[:2000]}") 
           else: 
            st.caption("⚠️ No standard README.md found in default repository branch.") 
          except Exception: 
           st.caption("⚠️ Unable to process project markdown data frames.") 
 
        st.session_state.vault_context = "\n\n===\n\n".join(temp_context)
        if fintech_weight >= bpo_weight and fintech_weight > 0: st.session_state.niche_brand = "capital_vantage"
        elif bpo_weight > fintech_weight: st.session_state.niche_brand = "transition_control"
        else: st.session_state.niche_brand = "general"
        st.rerun() 
     else: st.error(f"GitHub API Error. Status Code: {response.status_code}.") 
    except Exception as e: st.error(f"System sync connection error occurred: {str(e)}")
import streamlit as st

def handle_recruiter_chatbot(username):
  if st.session_state.niche_brand == "capital_vantage":
   st.header("🤖 CapitalVantage AI Auditor")
   st.write("Processing financial statement data structures and auditing tables.")
  elif st.session_state.niche_brand == "transition_control":
   st.header("🤖 TransitionControl Governance Center")
   st.write("Scanning migration pathways to completely eliminate operational risk gaps.")
  else:
   st.header("💬 Chat with Repositories") 
   st.write("Hiring managers can interview your codebase vector data spaces instantly.") 
 
  user_api_key = st.text_input("🔒 Enter Google Gemini API Key to activate AI responses:", type="password", placeholder="AIzaSy...") 
  chat_container = st.container(height=350) 
 
  for message in st.session_state.chat_history: 
   with chat_container.chat_message(message["role"]): 
    st.write(message["content"]) 
 
  if recruiter_prompt := st.chat_input("Ask about technologies or data project metrics..."): 
   with chat_container.chat_message("user"): 
    st.write(recruiter_prompt) 
   st.session_state.chat_history.append({"role": "user", "content": recruiter_prompt}) 
 
   with chat_container.chat_message("assistant"): 
    with st.spinner("Processing live data tokens..."): 
     cleaned_key = user_api_key.strip() 
     if cleaned_key: 
      try: 
       from google import genai 
       client = genai.Client(api_key=cleaned_key, http_options={'api_version': 'v1'}) 
 
       # SYSTEM INSTRUCTIONS ADAPT TO MATCH THE ACTIVE DOMAIN PORTFOLIO
       if st.session_state.niche_brand == "capital_vantage":
        niche_instruction = "You are an autonomous FinTech Financial Analyst and Auditing Agent. Review metrics for precision and transaction validity."
       elif st.session_state.niche_brand == "transition_control":
        niche_instruction = "You are an expert BPO Migration Auditor. Identify processing gaps, risk vectors, and project governance criteria."
       else:
        niche_instruction = f"You are the expert AI technical assistant representing developer {username}."
        
       system_instruction = ( 
        f"{niche_instruction} " 
        f"Answer recruiter questions professionally, confidently, and concisely. Use ONLY the following verified " 
        f"repository context facts to back up your claims. If information is missing, state truthfully that it is not " 
        f"explicitly detailed in the public documentation.\n\n[VERIFIED DATA RECORDS]:\n{st.session_state.vault_context}" 
       ) 
 
       response = client.models.generate_content( 
        model='gemini-2.5-flash', 
        contents=f"{system_instruction}\n\nUser Question: {recruiter_prompt}" 
       ) 
       bot_reply = response.text 
      except Exception as sdk_err: 
       bot_reply = f"⚠️ Google SDK execution fault occurred: {str(sdk_err)}" 
     else: 
      bot_reply = f"Based on {username}'s public repositories, they possess verified experience working with production data pipelines. (⚠️ Sandbox Mode. Provide a `Gemini API Key` above to unlock true conversational generations)." 
 
     st.write(bot_reply) 
     st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
