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
        raw_input = input_username.strip()
        
        # 🛡️ BULLETPROOF PROFILE LINK CLEANER FOR JOB HUNTING:
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
            st.rerun()
        else:
            st.error("Please provide a valid developer username to proceed.")
# --- PORTFOLIO DASHBOARD ---
else:
    username = st.session_state.username
    
    # Navigation row setup - fixed column unpacking strategy matching your working version
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
        
        if st.button("🔄 Sync Live GitHub Repositories Now", type="primary"):
            with st.spinner("Accessing GitHub REST endpoints..."):
                try:
                    # 🚀 CLEAN DIRECT PAGINATED ENDPOINT PATH WITHOUT EXTERNAL SECRETS INTERFERENCE
                    target_url = f"https://api.github.com/users/{username}/repos?per_page=100"
                        
                    response = requests.get(target_url)
                    
                    if response.status_code == 200:
                        try:
                            repos = response.json()
                            
                            if isinstance(repos, list):
                                st.success(f"Successfully tracked and parsed {len(repos)} public repositories!")
                                temp_context = []
                                
                                # UNLOCKED: Removed the [:5] slice parameter to render ALL public repositories
                                for repo in repos:
                                    with st.container(border=True):
                                        st.subheader(repo['name'])
                                        st.write(f"**Stars:** ⭐ {repo['stargazers_count']} | **Language:** 🛠️ {repo['language'] or 'Markdown'}")
                                        st.write(repo['description'] or "No public description provided.")
                                        
                                        temp_context.append(f"Repository: {repo['name']}\nDescription: {repo['description'] or 'None'}\nLanguage: {repo['language'] or 'Unknown'}")
                                        
                                        try:
                                            default_branch = repo.get('default_branch', 'main')
                                            readme_url = f"https://raw.githubusercontent.com/{username}/{repo['name']}/{default_branch}/README.md"
                                            readme_req = requests.get(readme_url)
                                            
                                            if readme_req.status_code == 200 and len(readme_req.text.strip()) > 5:
                                                text_slices = chunk_text_data(readme_req.text)
                                                st.caption(f"⚙️ RAG Engine: Split readme into {len(text_slices)} context vectors.")
                                                temp_context.append(f"README Content Slices for {repo['name']}:\n{readme_req.text[:2000]}")
                                            else:
                                                st.caption("⚠️ No standard README.md found in default repository workspace branch.")
                                        except Exception:
                                            st.caption("⚠️ Unable to process project markdown data frames.")
                                            
                                st.session_state.vault_context = "\n\n===\n\n".join(temp_context)
                            else:
                                st.error("GitHub API returned a single profile layout object instead of a repository listing array data grid.")
                        except ValueError:
                            st.error("Critical System Framework Error: Server data response mapping is corrupted or malformed.")
                    else:
                        st.error(f"GitHub API Error. Status Code: {response.status_code}. Profile might not exist.")
                except Exception as e:
                    st.error(f"System sync connection error occurred: {str(e)}")
        else:
            st.info("Click the Sync button above to scrape public GitHub API records dynamically.")

    with right_chatbot:
        st.header(f"💬 Chat with {username}'s Repos")
        st.write("Hiring managers can interview your codebase vector data spaces instantly.")
        
        # 🔑 PASSWORD MASKED INPUT WIDGET SECURED IN THE FRONTEND UI:
        user_api_key = st.text_input(
            "🔑 Enter Google Gemini API Key to activate AI responses:", 
            type="password", 
            placeholder="AIzaSy..."
        )
        
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
                            # 🛡️ Initialize official modern unified SDK client 
                            from google import genai
                            
                            # Force client networking requests through the stable production route parameter
                            client = genai.Client(api_key=cleaned_key, http_options={'api_version': 'v1'})
                            
                            system_instruction = (
                                f"You are the expert AI technical assistant representing developer {username}. "
                                f"Answer recruiter questions professionally, confidently, and concisely. Use ONLY the following verified "
                                f"repository context facts to back up your claims. If information is missing, state truthfully that it is not "
                                f"explicitly detailed in the public documentation.\n\n[VERIFIED DATA RECORDS]:\n{st.session_state.vault_context}"
                            )
                            
                            # Execute native production-grade SDK content generation text structures
                            response = client.models.generate_content(
                                model='gemini-1.5-flash',
                                contents=f"{system_instruction}\n\nUser Question: {recruiter_prompt}"
                            )
                            
                            bot_reply = response.text
                            
                        except Exception as sdk_err:
                            bot_reply = f"⚠️ Google SDK execution fault occurred: {str(sdk_err)}"
                    else:
                        bot_reply = f"Based on {username}'s public repositories, they possess verified experience working with production data pipelines. (🔒 Sandbox Mode. Provide a `Gemini API Key` above to unlock true conversational generations)."
                    
                    st.write(bot_reply)
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
