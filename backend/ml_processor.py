import os
import joblib
import requests
import streamlit as st
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

def chunk_text_data(text, max_chars=800): 
    """
    Slices long project documentation or README text frames into manageable chunks.
    """
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
    """
    Scans repository metadata on initial sync, automatically builds target 
    supervised labels using text patterns, and trains a scikit-learn model.
    """
    dataset_descriptions = []
    dataset_labels = []
    
    for repo in repos:
        desc = repo.get("description", "") or ""
        name = repo.get("name", "").lower()
        combined_text = f"{name}. {desc.lower()}"
        if not desc: 
            continue
        
        # Supervised labeling assignment via context keyword classification
        assigned_label = "general_portfolio"
        if any(w in combined_text for w in ["invoice", "ledger", "tax", "banking", "finance", "capital", "vantage", "money"]):
            assigned_label = "capital_vantage"
        elif any(w in combined_text for w in ["migration", "workflow", "governance", "risk", "bpo", "control", "roadmap"]):
            assigned_label = "transition_control"
            
        if assigned_label != "general_portfolio":
            dataset_descriptions.append(f"{repo['name']}. {desc}")
            dataset_labels.append(assigned_label)
            
    # Compile the training pipeline once both distinct classes are present
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
    """
    Loads the trained model weights into server cache memory for speed.
    """
    if os.path.exists("industry_classifier.pkl"):
        return joblib.load("industry_classifier.pkl")
    return None

def run_dynamic_sync_pipeline(username):
    """
    Scrapes the public GitHub REST API, processes text vectors through the 
    ML model layer, and triggers the layout branding shifts.
    """
    # 1. Clean the incoming username parameter just in case
    username = username.replace("github.com", "").strip("/")
    
    with st.spinner("Accessing GitHub REST endpoints..."): 
        try: 
            # 🎯 FIXED: This must point to ://github.com...
            target_url = f"https://://github.com{username}/repos?per_page=100" 
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
                            if predicted == "capital_vantage": 
                                fintech_weight += 1
                            elif predicted == "transition_control": 
                                bpo_weight += 1
                          
                        with st.container(border=True): 
                            if assigned_tag == "capital_vantage": 
                                st.subheader(f"📈 {repo['name']} [Fintech Asset]")
                            elif assigned_tag == "transition_control": 
                                st.subheader(f"🛠️ {repo['name']} [BPO System]")
                            else: 
                                st.subheader(repo['name']) 
                               
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
                                    st.caption("⚠️ No standard README.md found in default branch.") 
                            except Exception: 
                                st.caption("⚠️ Unable to process project markdown data frames.") 
 
                    st.session_state.vault_context = "\n\n===\n\n".join(temp_context)
                    
                    # Update global niche state variables based on calculated classification weights
                    if fintech_weight >= bpo_weight and fintech_weight > 0: 
                        st.session_state.niche_brand = "capital_vantage"
                    elif bpo_weight > fintech_weight: 
                        st.session_state.niche_brand = "transition_control"
                    else: 
                        st.session_state.niche_brand = "general"
                    st.rerun() 
                else: 
                    st.error("GitHub API response layout configuration mismatch.") 
            else: 
                st.error(f"GitHub API Error. Status Code: {response.status_code}.") 
        except Exception as e: 
            st.error(f"System sync connection error occurred: {str(e)}")
