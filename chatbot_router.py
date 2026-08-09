import subprocess
import json
import os
import streamlit as st

def process_javascript_chat_engine(username, prompt, api_key):
    """
    Safely executes backend/api/chat.js via a Node.js runtime process,
    handling dependencies and passing layout variables.
    """
    cleaned_key = api_key.strip()
    if not cleaned_key:
        return f"Based on {username}'s public repositories, they possess verified experience working with production data pipelines. (⚠️ Sandbox Mode. Provide an API Key above to unlock true conversational generations)."

    # 🎯 SELF-HEALING AUTOMATION LAYER: Installs node_modules if they are missing on Streamlit Cloud
    if not os.path.exists("node_modules"):
        with st.spinner("Initializing first-time Node.js production dependencies (npm install)..."):
            try:
                subprocess.run(["npm", "install"], check=True, capture_output=True, text=True)
            except Exception as e:
                return f"⚠️ Automated npm initialization package deployment failed: {str(e)}"

    # 1. Establish custom system personas matching your ML layout state weights
    if st.session_state.niche_brand == "capital_vantage":
        niche_instruction = "You are an autonomous FinTech Financial Analyst and Auditing Agent. Review metrics for precision and transaction validity."
    elif st.session_state.niche_brand == "transition_control":
        niche_instruction = "You are an expert BPO Migration Auditor. Identify processing gaps, risk vectors, and project governance criteria."
    else:
        niche_instruction = f"You are the expert AI technical assistant representing developer {username}."

    # 2. Package everything into a structured JSON payload to hand over to chat.js
    payload_matrix = {
        "username": username,
        "prompt": prompt,
        "apiKey": cleaned_key,
        "systemInstruction": niche_instruction,
        "vaultContext": st.session_state.vault_context
    }

    try:
        # Secure path navigation matching your exact repo tree structure
        target_js_script = os.path.join("backend", "api", "chat.js")
        
        # 3. Launch Node.js process to execute your chat.js logic
        process = subprocess.Popen(
            ["node", target_js_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Pipe the input payload data securely into standard input stream
        stdout, stderr = process.communicate(input=json.dumps(payload_matrix))
        
        if process.returncode == 0:
            return stdout.strip()
        else:
            return f"⚠️ JavaScript Execution Fault Error: {stderr.strip()}"
            
    except Exception as e:
        return f"⚠️ Failed to spawn Node.js runtime thread connection pipeline: {str(e)}"
