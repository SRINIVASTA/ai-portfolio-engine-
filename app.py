import streamlit as st 
import requests 
import sys
import os



# High-visibility centered title and status banner
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #FAFAFA; margin-bottom: 5px;">🚀 AI Portfolio Engine</h1>
        <p style="color: #FF4B4B; font-size: 18px; font-weight: bold; margin-top: 0; margin-bottom: 15px;">
            Automated Developer Portfolio Hub & Isolated RAG Chatbot
        </p>
        <div style="display: inline-block; background-color: #262730; padding: 8px 16px; border-radius: 5px; border: 1px solid #FF4B4B;">
            <span style="color: #FAFAFA; font-weight: 500;">✓ Verified Production Architecture Integration Enabled</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="text-align: center; color: #FAFAFA; font-size: 14px; margin-bottom: 20px;">
        <strong>© 2026 T A Srinivas. All Rights Reserved. For portfolio viewing only.</strong>
    </div>
    """,
    unsafe_allow_html=True
)


# --- CRITICAL WORKSPACE MODULE RESOLUTION SYSTEM ---
root_workspace = os.path.dirname(os.path.abspath(__file__))
if root_workspace not in sys.path:
    sys.path.insert(0, root_workspace)

# Force strict dark mode styling layout
st.set_page_config(page_title="AI Portfolio Engine", layout="wide", initial_sidebar_state="collapsed") 

# --- FIXED SUBDIRECTORY PATH CHANNEL IMPORTING ---
from backend.ml_processor import run_dynamic_sync_pipeline
from chatbot_router import process_javascript_chat_engine

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
if "sync_completed" not in st.session_state:
 st.session_state.sync_completed = False
if "repos_data" not in st.session_state:
 st.session_state.repos_data = []

# --- LANDING PAGE (SaaS Entry Point) --- 
if not st.session_state.logged_in: 
 st.title("🚀 Turn Your GitHub Into An AI Portfolio") 
 st.subheader("Deploy a self-updating website with an interactive recruiter chatbot trained on your code.") 
 st.write("---") 
 
 st.write("### Multi-User Gateway Authentication") 
 input_username = st.text_input("Enter GitHub Username or Profile Link:", placeholder="e.g., srinivasta or https://github.com") 
 
 if st.button("Sign In to Portfolio", type="primary"): 
  raw_input = input_username.strip() 
 
  if "/" in raw_input:
      cleaned_username = [piece for piece in raw_input.split("/") if piece][-1]
  else:
      cleaned_username = raw_input
      
  cleaned_username = cleaned_username.replace("github.com", "").replace("https:", "").replace("http:", "")
  cleaned_username = cleaned_username.strip("/")
  cleaned_username = cleaned_username.strip()
 
  if cleaned_username and len(cleaned_username) > 1: 
   st.session_state.logged_in = True 
   st.session_state.username = cleaned_username 
   st.session_state.vault_context = "" 
   st.session_state.chat_history = [] 
   st.session_state.niche_brand = "general"
   st.session_state.sync_completed = False
   st.session_state.repos_data = []
   st.rerun() 
  else: 
   st.error("Please provide a valid developer username to proceed.") 

# --- PORTFOLIO DASHBOARD --- 
else: 
 session_user = str(st.session_state.username).strip()
 if "/" in session_user:
     session_user = [piece for piece in session_user.split("/") if piece][-1]
 
 session_user = session_user.replace("github.com", "").replace("https:", "").replace("http:", "")
 session_user = session_user.strip("/")
 session_user = session_user.strip()
 st.session_state.username = session_user

 username = st.session_state.username 
 
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
   # st.title("🚀 AI Portfolio Engine")
   # st.subheader("Automated Developer Portfolio Hub & Isolated RAG Chatbot")
  # else:
   st.title(f"✨ Developer Portfolio: {username}") 
 with col2: 
  if st.button("Log Out of System", type="secondary", use_container_width=True): 
   st.session_state.logged_in = False 
   st.session_state.username = None 
   st.session_state.chat_history = [] 
   st.session_state.vault_context = "" 
   st.session_state.niche_brand = "general"
   st.session_state.sync_completed = False
   st.session_state.repos_data = []
   st.rerun() 
 
 # st.write("`✓ Verified Production Architecture Integration Enabled`") 
 # st.write("---") 
 
 left_layout, right_chatbot = st.columns(2, gap="large") 
 
 with left_layout: 
  st.header("📁 Core Tracked Repositories") 
  if st.button("🔄 Sync Live GitHub Repositories Now", type="primary"): 
   run_dynamic_sync_pipeline(username)
   
  if st.session_state.sync_completed and st.session_state.repos_data:
   st.success("Repository context matrices successfully synced and written to session memory!")
   
   def get_ml_priority(repo):
       tag = repo.get('tag', 'general')
       if tag == "capital_vantage":
           return 1
       elif tag == "transition_control":
           return 2
       return 3

   ml_sorted_repos = sorted(st.session_state.repos_data, key=get_ml_priority)

   # =========================================================================
   # 🤖 THE ZERO-TOUCH DISK AUTOMATION OVERRIDE & WEB PORT LINK HOOK
   # =========================================================================
   from backend.compiler import auto_generate_portfolio_index
   raw_compiled_html = auto_generate_portfolio_index(username, ml_sorted_repos)
   
   st.write("---")
   st.subheader("🎉 Portfolio Website Generation Active!")
   st.download_button(
       label="📥 Download and Save My Portfolio (`index.html`)",
       data=raw_compiled_html,
       file_name="index.html",
       mime="text/html",
       use_container_width=True
   )
   
   with st.expander("👀 View Interactive Portfolio Hub Layout Directly Inside App", expanded=True):
       import streamlit.components.v1 as components
       components.html(raw_compiled_html, height=800, scrolling=True)
   st.write("---")
   # =========================================================================

   for repo in ml_sorted_repos:
    with st.container(border=True):
     if repo['tag'] == "capital_vantage": 
      st.subheader(f"📈 {repo['name']} [Fintech Asset]")
     elif repo['tag'] == "transition_control": 
      st.subheader(f"🛠️ {repo['name']} [BPO System]")
     else: 
      st.subheader(repo['name']) 
      
     st.write(f"**Language:** 📝 {repo['language']}")
     st.write(repo['description'])
  else: 
   st.info("Click the Sync button above to scrape public GitHub API records dynamically.") 
   
 with right_chatbot: 
  if st.session_state.niche_brand == "capital_vantage":
   st.header("🤖 CapitalVantage AI Auditor")
   st.write("Processing financial statement data structures and auditing tables.")
  elif st.session_state.niche_brand == "transition_control":
   st.header("🤖 TransitionControl Governance Center")
   st.write("Querying synced repository matrices to eliminate operational migration and risk gaps.")
  else:
   st.header("💬 Chat with Repositories") 
   st.write("Hiring managers can interview your codebase vector data spaces instantly.") 
 
  user_api_key = st.text_input("🔒 Enter API Token to activate JavaScript response layers:", type="password", placeholder="AIzaSy...") 
  chat_container = st.container(height=350) 
 
  for message in st.session_state.chat_history: 
   with chat_container.chat_message(message["role"]): 
    st.write(message["content"]) 
 
  if recruiter_prompt := st.chat_input("Ask about technologies or data project metrics..."): 
   with chat_container.chat_message("user"): 
    st.write(recruiter_prompt) 
   st.session_state.chat_history.append({"role": "user", "content": recruiter_prompt}) 
 
   with chat_container.chat_message("assistant"): 
    with st.spinner("Invoking JavaScript Subprocess Worker Layer..."): 
     bot_reply = process_javascript_chat_engine(username, recruiter_prompt, user_api_key)
     st.write(bot_reply) 
     st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})


# High-visibility fixed footer with professional contact links
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #262730; /* Matches your secondary background */
        color: #FAFAFA;            /* Matches your theme text color */
        text-align: center;
        font-size: 13px;
        padding: 12px 0;
        z-index: 999999;           /* Forces footer to stay on top of everything */
        border-top: 1px solid #FF4B4B; /* Adds a thin red line accent */
    }
    .footer a {
        color: #FF4B4B;            /* Uses your primary theme red color for links */
        text-decoration: none;
        margin: 0 10px;
        font-weight: bold;
    }
    .footer a:hover {
        text-decoration: underline;
        color: #FAFAFA;            /* Turns white when hovered */
    }
    .footer-separator {
        color: #666;
        margin: 0 5px;
    }
    /* Adds padding to the bottom of the page container so content isn't blocked */
    .main .block-container {
        padding-bottom: 70px;
    }
    </style>
    <div class="footer">
        <span><strong>© 2026 T A Srinivas.</strong> All Rights Reserved. Strictly for portfolio viewing purposes.</span>
        <span class="footer-separator">|</span>
        <a href="https://www.linkedin.com/in/srinivas-t-a-557637119/" target="_blank">LinkedIn Profile</a>
        <span class="footer-separator">|</span>
        <a href="mailto:tasrinivass@gmail.com">Contact Me</a>
    </div>
    """,
    unsafe_allow_html=True
)
