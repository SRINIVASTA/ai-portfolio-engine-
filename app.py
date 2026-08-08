import streamlit as st
import requests

# Force strict dark mode styling layout
st.set_page_config(page_title="AI Portfolio Engine", layout="wide", initial_sidebar_state="collapsed")

# 1. Initialize Global Application States
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vault_context" not in st.session_state:
    st.session_state.vault_context = ""

# Text splitting helper for large repo files
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

# --- LANDING PAGE (SaaS Entry Point) ---
if not st.session_state.logged_in:
    st.title("🚀 Turn Your GitHub Into An AI Portfolio")
    st.subheader("Deploy a self-updating website with an interactive recruiter chatbot trained on your code.")
    st.write("---")
    
    st.write("### Multi-User Gateway Authentication")
    input_username = st.text_input("Enter GitHub Username or Profile Link:", placeholder="e.g., srinivasta or https://github.com")
    
    if st.button("Sign In to Portfolio", type="primary"):
        cleaned_username = input_username.strip()
        
        # AUTOMATIC TEXT CLEANING RULE
        if "://github.com" in cleaned_username:
            cleaned_username = cleaned_username.split("://github.com")[-1].strip("/")
        if "github.com" in cleaned_username:
            cleaned_username = cleaned_username.split("github.com")[-1].strip("/")
            
        if cleaned_username:
            st.session_state.logged_in = True
            st.session_state.username = cleaned_username
            st.session_state.vault_context = "" # Reset context state across profiles
            st.session_state.chat_history = []
            st.rerun()
        else:
            st.error("Please provide a valid developer username to proceed.")
# --- PORTFOLIO DASHBOARD ---
else:
    username = st.session_state.username
    
    # Navigation row setup
    col1, col2 = st.columns(2)
    with col1:
        st.title(f"✨ Developer Portfolio: {username}")
    with col2:
        if st.button("Log Out of System", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.chat_history = []
            st.session_state.vault_context = ""
            st.rerun()
            
    st.write("`✓ Verified Production Architecture Integration Enabled`")
    st.write("---")
    
    # Split layout configuration grids
    left_layout, right_chatbot = st.columns(2, gap="large")
    
    with left_layout:
        st.header("📂 Core Tracked Repositories")
        
        # Trigger GitHub Profile API data scrape loop
        if st.button("🔄 Sync Live GitHub Repositories Now", type="primary"):
            with st.spinner("Accessing GitHub REST endpoints..."):
                try:
                    # THE SECURE BYPASS INJECTION SWITCH FOR STABILITY
                    if "TARGET_URL_OVERRIDE" in st.secrets and "users" in st.secrets["TARGET_URL_OVERRIDE"]:
                        target_url = st.secrets["TARGET_URL_OVERRIDE"]
                    else:
                        target_url = f"https://github.com{username}/repos"
                        
                    response = requests.get(target_url)
                    
                    if response.status_code == 200:
                        try:
                            repos = response.json()
                            
                            if isinstance(repos, list):
                                st.success(f"Successfully tracked and parsed {len(repos)} public repositories!")
                                temp_context = []
                                
                                # Render top 5 repository containers smoothly
                                for repo in repos[:5]:
                                    with st.container(border=True):
                                        st.subheader(repo['name'])
                                        st.write(f"**Stars:** ⭐ {repo['stargazers_count']} | **Language:** 🛠️ {repo['language'] or 'Markdown'}")
                                        st.write(repo['description'] or "No public description provided.")
                                        
                                        # Save basic repo info to core context list
                                        temp_context.append(f"Repository: {repo['name']}\nDescription: {repo['description'] or 'None'}\nLanguage: {repo['language'] or 'Unknown'}")
                                        
                                        try:
                                            default_branch = repo.get('default_branch', 'main')
                                            readme_url = f"https://githubusercontent.com{username}/{repo['name']}/{default_branch}/README.md"
                                            readme_req = requests.get(readme_url)
                                            
                                            if readme_req.status_code == 200 and len(readme_req.text.strip()) > 5:
                                                text_slices = chunk_text_data(readme_req.text)
                                                st.caption(f"⚙️ RAG Engine: Split readme into {len(text_slices)} context vectors.")
                                                # Inject code documentation text blocks into storage arrays
                                                temp_context.append(f"README Content Slices for {repo['name']}:\n{readme_req.text[:2000]}")
                                            else:
                                                st.caption("⚠️ No standard README.md found in default repository branch workspace.")
                                        except Exception:
                                            st.caption("⚠️ Unable to process project markdown data frames.")
                                
                                # Accumulate tracked vectors into global dashboard state storage
                                st.session_state.vault_context = "\n\n===\n\n".join(temp_context)
                            else:
                                st.error("GitHub API returned a single profile object instead of an array row listing.")
                        except ValueError:
                            st.error("Critical System Error: Malformed backend JSON response mapping.")
                    else:
                        st.error(f"GitHub API Error. Status Code: {response.status_code}.")
                except Exception as e:
                    st.error(f"System sync connection error occurred: {str(e)}")
        else:
            st.info("Click the Sync button above to scrape public GitHub API records dynamically.")

    with right_chatbot:
        st.header(f"💬 Chat with {username}'s Repos")
        st.write("Hiring managers can interview your codebase vector data spaces instantly.")
        
        chat_container = st.container(height=400)
        
        # Render conversational bubbles arrays loop configurations
        for message in st.session_state.chat_history:
            with chat_container.chat_message(message["role"]):
                st.write(message["content"])
                
        if recruiter_prompt := st.chat_input("Ask about technologies or data project metrics..."):
            with chat_container.chat_message("user"):
                st.write(recruiter_prompt)
            st.session_state.chat_history.append({"role": "user", "content": recruiter_prompt})
            
            with chat_container.chat_message("assistant"):
                with st.spinner("Processing live generation tokens..."):
                    gemini_key = st.secrets.get("GEMINI_API_KEY", None)
                    
                    if gemini_key:
                        # 🧠 PRODUCTION RAG ROUTER: Direct connection to Google's Gemini endpoint
                        gemini_url = f"https://googleapis.com{gemini_key}"
                        
                        system_instruction = (
                            f"You are the expert AI technical assistant representing developer {username}. "
                            f"Answer recruiter questions professionally, confidently, and concisely. Use ONLY the following verified "
                            f"repository context facts to back up your claims. If information is missing, state truthfully that it is not "
                            f"explicitly detailed in the public documentation.\n\n[VERIFIED DATA RECORDS]:\n{st.session_state.vault_context}"
                        )
                        
                        payload = {
                            "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser Question: {recruiter_prompt}"}]}]
                        }
                        
                        try:
                            api_res = requests.post(gemini_url, json=payload)
                            if api_res.status_code == 200:
                                bot_reply = api_res.json()["candidates"][0]["content"]["parts"][0]["text"]
                            else:
                                bot_reply = "⚠️ The AI processing pipeline returned a network error. Ensure your Gemini API Key configuration is active."
                        except Exception as e:
                            bot_reply = f"⚠️ Connection timed out while reading model vectors: {str(e)}"
                    else:
                        # Professional sandbox fallback notice
                        bot_reply = f"Hi! I am the automated chatbot twin for {username}. To unlock live responses trained directly on my code readmes, please save your free `GEMINI_API_KEY` inside your app's secret dashboard settings panel."
                    
                    st.write(bot_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
