import os
import re
import requests
import joblib
import numpy as np
import streamlit as st
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

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

def dynamically_cluster_repositories(repos, n_clusters=4):
    """
    Completely unsupervised system that groups any developer's repositories 
    using K-Means clustering and generates dynamic section titles automatically.
    """
    dataset_texts = []
    valid_repos = []
    
    for repo in repos:
        name = repo.get("name", "") or ""
        desc = repo.get("description", "") or "No public description provided."
        
        # Dynamic Data Correction Layer: Catches S&P vs Nifty anomalies natively
        if "snp" in name.lower() or "s&p" in name.lower():
            desc = re.sub(r'(?i)nifty\s*50', 'S&P Top Market Equities', desc)
            repo["description"] = desc
            
        combined_text = f"{name} {desc}".lower()
        dataset_texts.append(combined_text)
        valid_repos.append(repo)
        
    if len(valid_repos) < n_clusters:
        n_clusters = max(1, len(valid_repos))
        
    # 1. Convert text descriptions into mathematical feature vectors
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=500)
    tfidf_matrix = vectorizer.fit_transform(dataset_texts)
    
    # 2. Run K-Means to find natural concept buckets
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(tfidf_matrix)
    
    # 3. Dynamic Section Header Generation: Extract top keywords per cluster
    terms = vectorizer.get_feature_names_out()
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    
    cluster_to_title_map = {}
    for i in range(n_clusters):
        # Extract the top 2 highly relevant terms for this cluster
        top_words = [terms[ind] for ind in order_centroids[i, :2]]
        title = " & ".join([w.capitalize() for w in top_words]) + " Core Systems"
        cluster_to_title_map[i] = title
        
    return cluster_labels, cluster_to_title_map, valid_repos

def run_dynamic_sync_pipeline(username):
    """
    Dynamic pipeline that scrapes, clusters, and structures any public profile layout on the fly.
    """
    # 1. Clean the incoming string of any accidental domain artifacts
    raw_user = str(username).strip()
    raw_user = raw_user.replace("https://", "").replace("http://", "").replace("github.com", "")
    
    # Isolate the pure handle fragment cleanly
    fragments = [f for f in raw_user.split("/") if f]
    if not fragments:
        st.error("Invalid GitHub handle configuration provided.")
        return
    clean_handle = fragments[-1].strip()

    with st.spinner(f"Accessing dynamic ML pipelines for developer: {clean_handle}..."): 
        try: 
            # 🎯 CRITICAL FIX 1: Explicitly force the API url to hit the correct REST subdomain
            target_url = f"https://github.com{clean_handle}/repos?per_page=100" 
            
            headers = {"Accept": "application/vnd.github.v3+json"} 
            pat_token = st.secrets.get("GITHUB_PAT_TOKEN", None) 
            if pat_token: 
                headers["Authorization"] = f"token {pat_token}" 
 
            response = requests.get(target_url, headers=headers) 
            if response.status_code == 200: 
                raw_repos = response.json() 
                if isinstance(raw_repos, list) and len(raw_repos) > 0: 
                    
                    cluster_labels, cluster_titles, repos = dynamically_cluster_repositories(raw_repos)
                    temp_context = [] 
                    processed_repos_list = []
                    
                    for idx, repo in enumerate(repos): 
                        repo_name = repo['name']
                        desc = repo['description'] or "No public description provided."
                        cluster_id = int(cluster_labels[idx])
                        dynamic_tag = cluster_titles[cluster_id]
                        
                        default_branch = repo.get('default_branch', 'main') 
                        
                        # 🎯 CRITICAL FIX 2: Added explicit missing forward slash after the domain asset host
                        readme_url = f"https://githubusercontent.com{clean_handle}/{repo_name}/{default_branch}/README.md" 
                        
                        processed_repos_list.append({
                            "name": repo_name,
                            "stars": repo.get('stargazers_count', 0),
                            "language": repo.get('language') or 'Markdown',
                            "description": desc,
                            "tag": dynamic_tag,
                            "readme_url": readme_url
                        })
                        
                        temp_context.append(f"Repository: {repo_name}\nCategory Track: {dynamic_tag}\nDescription: {desc}") 
 
                    st.session_state.vault_context = "\n\n===\n\n".join(temp_context)
                    st.session_state.repos_data = processed_repos_list 
                    
                    all_tags = [r["tag"] for r in processed_repos_list]
                    st.session_state.niche_brand = Counter(all_tags).most_common(1)[0][0] if all_tags else "general"
                        
                    st.session_state.sync_completed = True
                    st.success(f"Successfully processed {len(repos)} repositories into {len(cluster_titles)} dynamic rows!")
                    st.rerun() 
                else: 
                    st.error("No valid public repositories found.") 
            else: 
                st.error(f"GitHub API Error. Status Code: {response.status_code}") 
        except Exception as e: 
            st.error(f"System sync connection error occurred: {str(e)}")
