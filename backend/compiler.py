import os
import re

def auto_generate_portfolio_index(username, ml_sorted_repos):
    """
    Advanced compiler engine matching the official AI-Portfolio-Hub structure.
    Features a strict markdown block scrubber to strip away residual terminal
    setup text blocks (git clone, cd, pip install) leaking from README.md records.
    """
    featured_html = ""
    tracked_html = ""
    unassigned_html = ""
    valid_idx = 0
    
    # Clean up the username parameter to prevent path fractures
    clean_user = str(username).strip().strip('/')
    
    for repo in ml_sorted_repos:
        name = repo.get('name', 'Unnamed Asset').strip()
        lang = repo.get('language', 'Python')
        desc = repo.get('description', '')
        tag = repo.get('tag', 'general')
        
        # Capture the official "About Website" URL property from the GitHub payload
        homepage_url = repo.get('homepage', '')
        homepage_url = str(homepage_url).strip() if homepage_url else ""
        
        # Skip processing completely if description field is empty
        if not desc or "no public description" in str(desc).lower():
            continue
            
        desc_str = str(desc).strip()

        # =========================================================================
        # 🤖 1. DYNAMICALLY EXTRACT LIVE WEBSITE LINK FIRST (FIXED PIPELINE ORDER)
        # =========================================================================
        # Pull text-embedded links safely before terminal scrubber commands slice the string apart
        extracted_url_match = re.search(r'(https?://[^\s#]+)', desc_str)
        
        if extracted_url_match:
            live_streamlit_url = extracted_url_match.group(1).strip().rstrip('.,;)(')
            desc_str = desc_str.replace(extracted_url_match.group(1), '').strip()
        elif homepage_url and homepage_url.startswith("http"):
            # Fallback to the authentic GitHub metadata URL field dynamically
            live_streamlit_url = homepage_url
        else:
            # Clean, dynamic template fallback for any multi-tenant user
            if str(lang).lower() == "python" or "streamlit" in name.lower():
                live_streamlit_url = f"https://streamlit.io{clean_user}/{name}"
            else:
                live_streamlit_url = f"https://github.com{clean_user}/{name}"

        # =========================================================================
        # 🎯 CRITICAL SYSTEM SCRUBBER: NOW SAFE TO REMOVE RESIDUAL TERMINAL TEXT
        # =========================================================================
        # Since the URL is safely stored in memory, we can safely clean the description string
        for filter_term in ["git clone", "cd ", "pip install", "streamlit run", "Clone the repository"]:
            if filter_term in desc_str:
                # Isolate only the clean text before the terminal instructions start
                desc_str = desc_str.split(filter_term)[0].strip()
                
        # Clean up any residual markdown headers, bullet symbols, or dangling lines
        desc_str = re.sub(r'(###?\s+.*|#.*)', '', desc_str) # Strips markdown headings
        desc_str = re.sub(r'(-\s+\*\*.*|\*\s+\*\*.*)', '', desc_str) # Strips list headers
        desc_str = desc_str.strip().rstrip(':-#* ')
        
        # Double check to verify we still have a usable description card paragraph after filtering
        if len(desc_str) < 5:
            continue
        # =========================================================================

        # 🤖 2. PARSE REPOSITORY TOPICS DYNAMICALLY
        topics = repo.get('topics', [])
        if not topics:
            # Multi-tenant context baseline topics mapping
            topics = ["streamlit", "python", "data-science", "machine-learning"]
                
        topics_html = "".join([f'<span style="background:#21262d; color:#8b949e; border:1px solid #30363d; padding:2px 6px; border-radius:4px; font-size:10px; font-family:monospace; margin-right:5px;">#{t}</span>' for t in topics[:4]])

        # Dynamic labeling based on language and keywords
        if "prediction" in name.lower() or "predictor" in name.lower() or "forecast" in name.lower():
            label_text = "AI Price Predictor System"
            icon_marker = "📈 📉 📊"
        elif "agent" in name.lower() or "bot" in name.lower() or "rag" in name.lower():
            label_text = "AI Framework Agent"
            icon_marker = "⚡ 🤖 🚀"
        elif str(lang).lower() == "python":
            label_text = "Python Execution Engine"
            icon_marker = "🌐 📊 🚀"
        else:
            label_text = "Matrix Component Layer"
            icon_marker = "⚙️ 🔧 🚀"

        # --- TRACK 1: FEATURED HIGH-DENSITY PROJECTS LAYER ---
        if valid_idx < 4 and (tag in ["capital_vantage", "transition_control"] or "streamlit" in name.lower() or "agent" in name.lower() or "predict" in name.lower()):
            featured_html += f"""
                <div style="background:#161b22; border:1px solid #30363d; padding:24px; border-radius:12px; margin-bottom:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                        <h3 style="margin:0; color:#fff; font-size:1.25rem;">{icon_marker} {name}: {label_text}</h3>
                        <a href="https://github.com{clean_user}/{name}" target="_blank" style="color:#58a6ff; text-decoration:none; font-weight:600; font-size:14px;">💻 View Source Code ↗</a>
                    </div>
                    <div style="margin:8px 0 12px 0;">{topics_html}</div>
                    <p style="color:#8b949e; line-height:1.6; margin:0 0 15px 0; font-size:14.5px;">{desc_str}</p>
                    
                    <a href="{live_streamlit_url}" target="_blank" style="display:inline-block; background:#238636; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:13px;">🌐 Live Interactive Web App: Launch Live Streamlit Dashboard</a>
                </div>
            """
            valid_idx += 1
        # --- TRACK 2: CORE REPOSITORIES GRID ---
        elif valid_idx < 10:
            track_title = "📊 FinTech Asset" if tag == "capital_vantage" else "🛠️ Business Intelligence" if tag == "transition_control" else "📁 Core Track Component"
            badge_bg = "#341212" if tag == "capital_vantage" else "#123034" if tag == "transition_control" else "#21262d"
            badge_color = "#ff7b72" if tag == "capital_vantage" else "#58a6ff" if tag == "transition_control" else "#8b949e"
            
            tracked_html += f"""
                <div style="background:#161b22; border:1px solid #30363d; padding:20px; border-radius:12px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:start; gap:10px; margin-bottom:8px;">
                            <h4 style="margin:0; color:#fff; font-size:1.1rem; max-width:70%; overflow:hidden; text-overflow:ellipsis;">{name}</h4>
                            <span style="background:{badge_bg}; color:{badge_color}; border:1px solid rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:11px; font-family:monospace; white-space:nowrap;">{lang}</span>
                        </div>
                        <div style="font-size:12px; color:#8b949e; font-family:monospace; margin-bottom:10px;">{track_title}</div>
                        <p style="color:#8b949e; font-size:13.5px; line-height:1.5; margin:0 0 15px 0;">{desc_str}</p>
                        <div style="margin-bottom:12px;">{topics_html}</div>
                    </div>
                    <div style="border-top:1px solid #21262d; padding-top:12px; display:flex; justify-content:space-between; align-items:center; margin-top:15px;">
                        <a href="{live_streamlit_url}" target="_blank" style="color:#34d399; text-decoration:none; font-size:13px; font-weight:bold;">Launch UI ↗</a>
                        <a href="https://github.com{clean_user}/{name}" target="_blank" style="color:#58a6ff; text-decoration:none; font-size:13px; font-weight:bold;">View Repo ↗</a>
                    </div>
                </div>
            """
            valid_idx += 1

        # --- TRACK 3: ADDITIONAL ARCHITECTURE UNASSIGNED MATRIX ---
        else:
            lang_color = "#34d399" if lang == "Python" else "#fbbf24" if lang == "HTML" else "#60a5fa"
            unassigned_html += f"""
                <a href="https://github.com{clean_user}/{name}" target="_blank" style="background:rgba(33,38,45,0.4); border:1px solid #30363d; padding:14px; border-radius:10px; text-decoration:none; display:block;">
                    <div style="color:#fff; font-weight:bold; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{name}</div>
                    <div style="color:{lang_color}; font-size:10px; margin-top:4px; font-family:monospace;">📝 {lang} Matrix Node</div>
                </a>
            """
            valid_idx += 1
    full_html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{clean_user} | AI & FinTech Portfolio</title>
    <style>
        body {{ background-color:#0d1117; color:#c9d1d9; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; margin:0; padding:40px 20px; }}
        .wrapper {{ max-width:1000px; margin:0 auto; }}
        .grid-layout {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:20px; margin-top:20px; }}
        .matrix-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:15px; margin-top:20px; }}
    </style>
</head>
<body>
    <div class="wrapper">
        <header style="border-bottom:1px solid #30363d; padding-bottom:30px; margin-bottom:40px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
            <div>
                <h1 style="margin:0; color:#fff; font-size:2rem;">🚀 Portfolio Engine Hub</h1>
                <p style="margin:8px 0 0 0; color:#8b949e;">Automated Identity Matrix Sync Engine for @{clean_user}</p>
            </div>
            <div style="background:#161b22; border:1px solid #30363d; padding:12px; border-radius:8px; font-family:monospace; font-size:12px; color:#ffb454;">
                🔒 Verified Matrix Core Layer Active
            </div>
        </header>

        <section style="margin-bottom:50px;">
            <h2 style="color:#fff; border-bottom:1px solid #21262d; padding-bottom:10px; font-size:1.5rem;">🌟 Featured Deployed Applications</h2>
            <div style="margin-top:20px;">{featured_html or '<p style="color:#8b949e;">No high-density featured assets found.</p>'}</div>
        </section>

        <section style="margin-bottom:50px;">
            <h2 style="color:#fff; border-bottom:1px solid #21262d; padding-bottom:10px; font-size:1.5rem;">📁 FinTech & Generative AI Production Tracks</h2>
            <div class="grid-layout">{tracked_html or '<p style="color:#8b949e;">No core grid assets available.</p>'}</div>
        </section>

        <section style="margin-bottom:40px;">
            <h2 style="color:#fff; border-bottom:1px solid #21262d; padding-bottom:10px; font-size:1.3rem;">📁 Additional Repository Architecture Matrix</h2>
            <div class="matrix-grid">{unassigned_html or '<p style="color:#8b949e;">No additional nodes indexed.</p>'}</div>
        </section>
    </div>
</body>
</html>"""

    # Sync and override the storage index document on disk automatically
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(full_html_output)
        
    return full_html_output
