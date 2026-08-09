import streamlit as st
from google import genai
from google.genai import types

def process_javascript_chat_engine(username, prompt, api_key):
    """
    Executes a direct Python connection to the Google GenAI model,
    completely replacing the error-prone Node.js subprocess.
    Optimized for Free-Tier token isolation and response completeness.
    """
    cleaned_key = api_key.strip()
    if not cleaned_key:
        return f"Based on {username}'s public repositories, they possess verified experience working with production data pipelines. (⚠️ Sandbox Mode. Provide an API Key above to unlock true conversational generations)."

    # 1. Establish custom system personas matching your ML layout state weights
    if st.session_state.niche_brand == "capital_vantage":
        niche_instruction = "You are an autonomous FinTech Financial Analyst and Auditing Agent. Review metrics for precision and transaction validity."
    elif st.session_state.niche_brand == "transition_control":
        # Strict free-tier gatekeeper rules appended directly to your BPO Auditor persona
        niche_instruction = (
            "You are an expert BPO Migration Auditor. Identify processing gaps, risk vectors, and project governance criteria.\n\n"
            "STRICT FREE-TIER OPTIMIZATION RULES:\n"
            "- Be highly concise. Use short, high-density sentences under 15 words.\n"
            "- Use bullet points and bold visual anchors for ultra-rapid scanning.\n"
            "- Limit the entire generation response strictly to under 350 words.\n"
            "- Max 2 processing gaps, max 2 risk vectors, and max 2 governance criteria.\n"
            "- Skip conversational fluff, introductory greetings, and conclusions. Go straight to data."
        )
    else:
        niche_instruction = f"You are the expert AI technical assistant representing developer {username}. Keep answers concise and high density."

    # 2. Extract repository context facts saved from the sync process
    final_context = st.session_state.get("vault_context", "") or "No custom repository documentation indexed."

    try:
        # 3. Direct Google GenAI Connection Pipeline
        client = genai.Client(api_key=cleaned_key)
        
        # Build strict execution constraints using the official SDK configuration container
        config = types.GenerateContentConfig(
            system_instruction=niche_instruction,
            temperature=0.1,  # Lower temperature locks down analytical structure and reduces token drifting
            max_output_tokens=1000  # Sets an absolute safe boundary to protect free tier rate windows
        )
        
        # Isolate the user prompt from system roles cleanly
        user_content = f"Contextual repository documentation facts:\n{final_context}\n\nUser Question: {prompt}"
        
        # Execute the live generation query using the configuration map
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_content,
            config=config
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "⚠️ Unable to parse streaming model generation content strings."
            
    except Exception as e:
        return f"⚠️ Google GenAI API Connection Pipeline Fault: {str(e)}"
