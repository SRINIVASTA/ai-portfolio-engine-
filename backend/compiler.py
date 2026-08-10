import os
import re

def auto_generate_portfolio_index(username, ml_sorted_repos):
    """
    Advanced multi-track portfolio compiler engine.
    Extracts loose domain targets dynamically before paragraph scrubbing sequences
    can break text variables apart, preserving unique deployment hashes.
    """
    image_studio_html = ""
    fintech_track_html = ""
    utility_track_html = ""
    unassigned_html = ""
    
    clean_user = str(username).strip().strip('/')
    
    for repo in ml_sorted_repos:
        name = repo.get('name', 'Unnamed Asset').strip()
        lang = repo.get('language', 'Python')
        desc = repo.get('description', '')
        tag = repo.get('tag', 'general')
        
        # Ingest the official GitHub "About Section" Website property from payload
        homepage_url = repo.get('homepage', '')
        homepage_url = str(homepage_url).strip() if homepage_url else ""
        
        if not desc or "no public description" in str(desc).lower():
            continue
            
        desc_str = str(desc).strip()

        # =========================================================================
        # 🤖 1. DYNAMICALLY EXTRACT PROTOCOL-AGNOSTIC LIVE APP LINKS
        # =========================================================================
        # Target full URLs containing http/https protocols first
        extracted_url_match = re.search(r'(https?://[^\s#]+)', desc_str)
        
        # Target loose domain string paths sitting bare inside text arrays
        loose_domain_match = re.search(r'([a-zA-Z0-9\-_]+\.streamlit\.app[^\s#]*)', desc_str)
        
        if extracted_url_match:
            live_streamlit_url = extracted_url_match.group(1).strip().rstrip('.,;) /')
            desc_str = desc_str.replace(extracted_url_match.group(1), '').strip()
        elif loose_domain_match:
            # Captures bare subdomains missing the protocol prefix dynamically
            captured_raw_url = loose_domain_match.group(1).strip().rstrip('.,;) /')
            live_streamlit_url = f"https://{captured_raw_url}"
            desc_str = desc_str.replace(loose_domain_match.group(1), '').strip()
        elif homepage_url and homepage_url.startswith("http"):
            live_streamlit_url = homepage_url
        else:
            # Dynamic tenant format fallback if no custom link is declared anywhere
            if str(lang).lower() == "python" or "streamlit" in name.lower():
                live_streamlit_url = f"https://{name.lower()}-{clean_user.lower()}.streamlit.app/"
            else:
                live_streamlit_url = f"https://github.com{clean_user}/{name}"

        # =========================================================================
        # 🎯 CASE-INSENSITIVE SCRUBBER: SAFELY CLEAN TEXT ROWS
        # =========================================================================
        # The true URL is locked safely in memory, text cleanup won't break the links
        for filter_term in ["git clone", "cd ", "pip install", "streamlit run", "clone the repository"]:
            if filter_term in desc_str.lower():
                match_start = desc_str.lower().find(filter_term)
                desc_str = desc_str[:match_start].strip()
                
        desc_str = re.sub(r'(###?\s+.*|#.*)', '', desc_str) 
        desc_str = re.sub(r'(-\s+\*\*.*|\*\s+\*\*.*)', '', desc_str) 
        desc_str = desc_str.strip().rstrip(':-#* ')
        
        if len(desc_str) < 5:
            continue
        # =========================================================================

        # 🤖 2. PARSE REPOSITORY TOPICS DYNAMICALLY
        topics = repo.get('topics', [])
        if not topics:
            topics = ["streamlit", "python", "data-science", "machine-learning"]
                
        topics_html = "".join([f'<span style="background:#21262d; color:#8b949e; border:1px solid #30363d; padding:2px 6px; border-radius:4px; font-size:10px; font-family:monospace; margin-right:5px;">#{t}</span>' for t in topics[:4]])

        # Create your targeted visual component card layout with the fixed button link paths
        card_html = f"""
            <div style="background:#161b22; border:1px solid #30363d; padding:20px; border-radius:12px; display:flex; flex-direction:column; justify-content:space-between;">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:start; gap:10px; margin-bottom:8px;">
                        <h4 style="margin:0; color:#fff; font-size:1.1rem; max-width:70%; overflow:hidden; text-overflow:ellipsis;">{name}</h4>
                        <span style="background:#21262d; color:#8b949e; border:1px solid rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:11px; font-family:monospace; white-space:nowrap;">{lang}</span>
                    </div>
                    <p style="color:#8b949e; font-size:13.5px; line-height:1.5; margin:0 0 15px 0;">{desc_str}</p>
                    <div style="margin-bottom:12px;">{topics_html}</div>
                </div>
                <div style="border-top:1px solid #21262d; padding-top:12px; display:flex; justify-content:space-between; align-items:center; margin-top:15px;">
                    <a href="{live_streamlit_url}" target="_blank" style="color:#34d399; text-decoration:none; font-size:13px; font-weight:bold;">Launch UI ↗</a>
                    <a href="https://github.com{clean_user}/{name}" target="_blank" style="color:#58a6ff; text-decoration:none; font-size:13px; font-weight:bold;">View Repo ↗</a>
                </div>
            </div>
        """

        # Separate items across rows dynamically based on context names
        name_lower = name.lower()
        if "image" in name_lower or "photo" in name_lower or "bg-changer" in name_lower or "nanobanana" in name_lower:
            image_studio_html += card_html
        # 🌟 FIXED: Added missing 'or' operator before checking group expressions
        elif "stock" in name_lower or "predict" in name_lower or "trend" in name_lower or ("price" in name_lower or "fintech" in name_lower or tag == "capital_vantage"):
            fintech_track_html += card_html
        elif "agent" in name_lower or "bot" in name_lower or "downloader" in name_lower or "summarizer" in name_lower or tag == "transition_control":
            utility_track_html += card_html
        else:
            lang_color = "#34d399" if lang == "Python" else "#fbbf24" if lang == "HTML" else "#60a5fa"
            unassigned_html += f"""
                <a href="https://github.com{clean_user}/{name}" target="_blank" style="background:rgba(33,38,45,0.4); border:1px solid #30363d; padding:14px; border-radius:10px; text-decoration:none; display:block;">
                    <div style="color:#fff; font-weight:bold; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{name}</div>
                    <div style="color:{lang_color}; font-size:10px; margin-top:4px; font-family:monospace;">📝 {lang} Matrix Node</div>
                </a>
            """
    full_html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{clean_user} | AI & FinTech Portfolio</title>
    <style>
        body {{ background-color:#0d1117; color:#c9d1d9; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; margin:0; padding:40px 20px; }}
        .wrapper {{ max-width:1000px; margin:0 auto; }}
        .row-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap:20px; margin-top:20px; margin-bottom:40px; }}
        .matrix-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:15px; margin-top:20px; }}
        .section-title {{ color:#fff; border-bottom:1px solid #21262d; padding-bottom:10px; font-size:1.4rem; display:flex; align-items:center; gap:10px; }}
    </style>
</head>
<body>
    <div class="wrapper">
        <header style="border-bottom:1px solid #30363d; padding-bottom:30px; margin-bottom:40px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
            <div>
                <h1 style="margin:0; color:#fff; font-size:2rem;">🚀 Developer Portfolio Hub</h1>
                <p style="margin:8px 0 0 0; color:#8b949e;">Multi-Tenant Identity Architecture Sync for @{clean_user}</p>
            </div>
            <div style="background:#161b22; border:1px solid #30363d; padding:12px; border-radius:8px; font-family:monospace; font-size:12px; color:#ffb454;">
                🔒 Verified Matrix Core Layer Active
            </div>
        </header>

        <!-- ROW 1: GENERATIVE AI & IMAGE PROCESSING STUDIO -->
        {f'<section><h2 class="section-title">🖼️ Generative AI & Image Studios</h2><div class="row-grid">{image_studio_html}</div></section>' if image_studio_html else ''}

        <!-- ROW 2: FINTECH & PREDICTION ASSETS -->
        {f'<section><h2 class="section-title">📈 FinTech Market Analytics & Price Engines</h2><div class="row-grid">{fintech_track_html}</div></section>' if fintech_track_html else ''}

        <!-- ROW 3: AUTOMATED UTILITY SYSTEMS & AGENTS -->
        {f'<section><h2 class="section-title">🛠️ Operational Utility Systems & Automation</h2><div class="row-grid">{utility_track_html}</div></section>' if utility_track_html else ''}

        <!-- ROW 4: GENERAL ARCHITECTURE BACKLOG INDEX -->
        {f'<section style="margin-bottom:40px;"><h2 class="section-title" style="font-size:1.2rem;">📁 Additional Repository Matrix Nodes</h2><div class="matrix-grid">{unassigned_html}</div></section>' if unassigned_html else ''}
    </div>
</body>
</html>"""

    # Sync and override the storage index document on disk automatically
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(full_html_output)
        
    return full_html_output
