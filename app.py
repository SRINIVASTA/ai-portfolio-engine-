import streamlit as st 
import requests 
import sys
import os

# --- CRITICAL WORKSPACE MODULE RESOLUTION SYSTEM ---
# Appends root and backend folders to Python workspace channels
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

# --- LANDING PAGE (SaaS Entry Point) --- 
if not st.session_state.logged_in: 
 st.title("🚀 Turn Your GitHub Into An AI Portfolio") 
 st.subheader("Deploy a self-updating website with an interactive recruiter chatbot trained on your code.") 
 st.write("---") 
 
 st.write("### Multi-User Gateway Authentication") 
 input_username = st.text_input("Enter GitHub Username or Profile Link:", placeholder="e.g., srinivasta or https://github.com") 
 
 if st.button("Sign In to Portfolio", type="primary"): 
  raw_input = input_username.strip() 
 
  # 🎯 RE-ENGINEERED BULLETPROOF PROFILE LINK CLEANER FOR RECRUITMENT SAAS PLATFORMS: 
  cleaned_username = raw_input
  
  # Remove protocol prefixes safely if pasted
  cleaned_username = cleaned_username.replace("https://", "").replace("http://", "")
  
  # Remove the domain signature safely if pasted
  cleaned_username = cleaned_username.replace("github.com", "")
  
  # Remove any leading or trailing slashes left behind by the strip splits
  cleaned_username = cleaned_username.strip("/")
  
  # Final sanitation trim
  cleaned_username = cleaned_username.strip()
 
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
  if st.session_state.niche_brand == "capital_vantage":
   st.header("🤖 CapitalVantage AI Auditor")
   st.write("Processing financial statement data structures and auditing tables.")
  elif st.session_state.niche_brand == "transition_control":
   st.header("🤖 TransitionControl Governance Center")
   st.write("Scanning migration pathways to completely eliminate operational risk gaps.")
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
     # Hand over processing parameters directly to our chatbot pipeline router
     bot_reply = process_javascript_chat_engine(username, recruiter_prompt, user_api_key)
     st.write(bot_reply) 
     st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
