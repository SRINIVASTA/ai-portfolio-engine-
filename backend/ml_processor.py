# https://github.com
import os
import joblib
import requests
import streamlit as st
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================================================================
# MODULE 1: SYSTEM IMPORTS & DATA CHUNKING CORE
# =========================================================================

def chunk_text_data(text, max_chars=800):
    """Processes long text blobs into optimized logical token chunks."""
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
# =========================================================================
# MODULE 2: MACHINE LEARNING TRAINING & COMPONENT LOADERS
# =========================================================================

def self_train_and_bootstrap_model(repos):
    """Trains a Naive Bayes model on current repository fingerprints."""
    dataset_descriptions = []
    dataset_labels = []
    
    for repo in repos:
        desc = repo.get("description", "") or ""
        name = repo.get("name", "").lower()
        combined_text = f"{name}. {desc.lower()}"
        if not desc:
            continue
            
        assigned_label = "general_portfolio"
        if any(w in combined_text for w in ["invoice", "ledger", "tax", "banking", "finance", "capital", "vantage", "money"]):
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
    """Loads pre-trained industry model configuration weights from disk."""
    if os.path.exists("industry_classifier.pkl"):
        return joblib.load("industry_classifier.pkl")
    return None
# =========================================================================
# MODULE 3: REPOSITORY UTILITY CHANNELS & MAIN SYNC PIPELINE
# =========================================================================

def run_dynamic_sync_pipeline(username):
    """Executes network synchronization against the core GitHub API endpoint."""
    raw_user = str(username).strip()
    clean_handle = [x for x in raw_user.split("/") if x][-1] if "/" in raw_user else raw_user
    clean_handle = clean_handle.replace("github.com", "").strip("/")
    
    with st.spinner(f"Accessing GitHub data pipelines for user: {clean_handle}..."):
        try:
            target_url = f"https://github.com{clean_handle}/repos?per_page=100"
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
                    processed_repos_list = []
                    
                    classifier_pipeline = load_ml_classifier() or self_train_and_bootstrap_model(repos)
                    fintech_weight, bpo_weight = 0, 0
                    
                    for repo in repos:
                        desc = repo.get('description', '') or ""
                        text_context = f"{repo.get('name', '')}. {desc}"
                        assigned_tag = "general"
                        
                        if classifier_pipeline and desc:
                            predicted = classifier_pipeline.predict([text_context])
                            if hasattr(predicted, '__iter__') and not isinstance(predicted, str):
                                assigned_tag = str(predicted[0])
                            else:
                                assigned_tag = str(predicted)
                                
                        if assigned_tag == "capital_vantage": fintech_weight += 1
                        elif assigned_tag == "transition_control": bpo_weight += 1
                        
                        default_branch = repo.get('default_branch', 'main')
                        readme_url = f"https://githubusercontent.com{clean_handle}/{repo['name']}/{default_branch}/README.md"
                        
                        processed_repos_list.append({
                            "name": repo['name'],
                            "stars": repo['stargazers_count'],
                            "language": repo['language'] or 'Markdown',
                            "description": repo['description'] or "No public description provided.",
                            "tag": assigned_tag,
                            "readme_url": readme_url
                        })
                        temp_context.append(f"Repository: {repo['name']}\nDescription: {repo['description'] or 'None'}\nLanguage: {repo['language'] or 'Unknown'}")
                    
                    st.session_state.vault_context = "\n\n===\n\n".join(temp_context)
                    st.session_state.repos_data = processed_repos_list
                    
                    if fintech_weight >= bpo_weight and fintech_weight > 0: st.session_state.niche_brand = "capital_vantage"
                    elif bpo_weight > fintech_weight: st.session_state.niche_brand = "transition_control"
                    else: st.session_state.niche_brand = "general"
                    
                    st.session_state.sync_completed = True
                    st.rerun()
                else:
                    st.error("GitHub API response layout configuration mismatch.")
            else:
                st.error(f"GitHub API Error. Status Code: {response.status_code}. User profile might not exist.")
        except Exception as e:
            st.error(f"System sync connection error occurred: {str(e)}")
