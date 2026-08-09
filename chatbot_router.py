import streamlit as st
from google import genai
from google.genai import types

def process_javascript_chat_engine(username, prompt, api_key):
    """
    Executes a direct Python connection to the Google GenAI model,
    completely replacing the error-prone Node.js subprocess.
    """
    cleaned_key = api_key.strip()
    if not cleaned_key:
        return f"Based on {username}'s public repositories, they possess verified experience working with production data pipelines. (⚠️ Sandbox Mode. Provide an API Key above to unlock true conversational generations)."

    # 1. Establish custom system personas matching your ML layout state weights
    if st.session_state.niche_brand == "capital_vantage":
        niche_instruction = "You are an autonomous FinTech Financial Analyst and Auditing Agent. Review metrics for precision and transaction validity."
    elif st.session_state.niche_brand == "transition_control":
        niche_instruction = "You are an expert BPO Migration Auditor. Identify processing gaps, risk vectors, and project governance criteria."
    else:
        niche_instruction = f"You are the expert AI technical assistant representing developer {username}."

    # 2. Extract repository context facts saved from the sync process
    final_context = st.session_state.get("vault_context", "") or "No custom repository documentation indexed."

    try:
        # 3. Direct Google GenAI Connection Pipeline
        client = genai.Client(api_key=cleaned_key)
        
        # Format the combined instruction prompt structure
        combined_prompt = f"{niche_instruction}\n\nContextual repository documentation facts:\n{final_context}\n\nUser Question: {prompt}"
        
        # Execute an absolute live generation query over the fast gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=combined_prompt,
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "⚠️ Unable to parse streaming model generation content strings."
            
    except Exception as e:
        return f"⚠️ Google GenAI API Connection Pipeline Fault: {str(e)}"
