import os

def auto_generate_portfolio_index(username, ml_sorted_repos):
    """
    Scrapes sync matrices, outputs static site files, and returns a safe,
    browser-compliant HTML payload block for opening tab links.
    """
    featured_html = ""
    tracked_html = ""
    unassigned_html = ""
    
    for idx, repo in enumerate(ml_sorted_repos):
        name = repo.get('name', 'Unnamed Asset')
        stars = repo.get('stars', 0)
        lang = repo.get('language', 'Python')
        desc = repo.get('description', 'No public description matrix provided.')
        tag = repo.get('tag', 'general')
        
        # --- FEATURED TRACKS ---
        if idx < 4 and (tag in ["capital_vantage", "transition_control"] or "streamlit" in name.lower()):
            icon = "📈 💰 🚀" if tag == "capital_vantage" else "📈 📊 🚀" if tag == "transition_control" else "🖼️ ⚡ 🤖"
            label = "GenAI Financial Intelligence" if tag == "capital_vantage" else "AI-Driven BPO Intelligence" if tag == "transition_control" else "Streamlit Application"
            
            featured_html += f"""
                <div style="background:#161b22; border:1px solid #30363d; padding:24px; border-radius:12px; margin-bottom:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                        <h3 style="margin:0; color:#fff; font-size:1.25rem;">{icon} {name}: {label}</h3>
                        <a href="https://github.com{username}/{name}" target="_blank" style="color:#58a6ff; text-decoration:none; font-weight:600; font-size:14px;">💻 View Source Code ↗</a>
                    </div>
                    <p style="color:#8b949e; line-height:1.6; margin:15px 0; font-size:15px;">{desc}</p>
                    <a href="https://streamlit.app" target="_blank" style="display:inline-block; background:#238636; color:#fff; padding:8px 16px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:13px;">Launch Live Platform</a>
                </div>
            """
        # --- STANDARD CORE TRACKS ---
        elif idx < 10:
            track_title = "📊 Fintech Asset" if tag == "capital_vantage" else "🛠️ BPO System" if tag == "transition_control" else "📁 Core Track Component"
            badge_bg = "#341212" if tag == "capital_vantage" else "#123034" if tag == "transition_control" else "#21262d"
            badge_color = "#ff7b72" if tag == "capital_vantage" else "#58a6ff" if tag == "transition_control" else "#8b949e"
            
            tracked_html += f"""
                <div style="background:#161b22; border:1px solid #30363d; padding:20px; border-radius:12px; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <div style="display:flex; justify-content:space-between; align-items:start; gap:10px; margin-bottom:8px;">
                            <h4 style="margin:0; color:#fff; font-size:1.1rem; max-width:70%; overflow:hidden; text-overflow:ellipsis;">{name}</h4>
                            <span style="background:{badge_bg}; color:{badge_color}; border:1px solid rgba(255,255,255,0.1); padding:2px 8px; border-radius:4px; font-size:11px; font-family:monospace; white-space:nowrap;">{lang}</span>
                        </div>
                        <div style="font-size:12px; color:#8b949e; font-family:monospace; margin-bottom:10px;">{track_title} | ⭐ Stars: {stars}</div>
                        <p style="color:#8b949e; font-size:13.5px; line-height:1.5; margin:0 0 15px 0;">{desc}</p>
                    </div>
                    <div style="border-top:1px solid #21262d; padding-top:12px; text-align:right;">
                        <a href="https://github.com{username}/{name}" target="_blank" style="color:#58a6ff; text-decoration:none; font-size:13px; font-weight:bold;">View Repo ↗</a>
                    </div>
                </div>
            """
        # --- LONG TAIL UTILITIES ---
        else:
            lang_color = "#34d399" if lang == "Python" else "#fbbf24" if lang == "HTML" else "#60a5fa"
            unassigned_html += f"""
                <a href="https://github.com{username}/{name}" target="_blank" style="background:rgba(33,38,45,0.4); border:1px solid #30363d; padding:14px; border-radius:10px; text-decoration:none; display:block;">
                    <div style="color:#fff; font-weight:bold; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{name}</div>
                    <div style="color:{lang_color}; font-size:10px; margin-top:4px; font-family:monospace;">📝 {lang} Matrix Node</div>
                </a>
            """

    full_html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{username} Portfolio Hub</title>
    <style>
        body {{ background-color:#0d1117; color:#c9d1d9; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; margin:0; padding:40px 20px; }}
        .wrapper {{ max-width:1000px; margin:0 auto; }}
        .grid-layout {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-top:20px; }}
        .matrix-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:15px; margin-top:20px; }}
    </style>
</head>
<body>
    <div class="wrapper">
        <header style="border-bottom:1px solid #30363d; padding-bottom:30px; margin-bottom:40px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:20px;">
            <div>
                <h1 style="margin:0; color:#fff; font-size:2rem;">🚀 AI Portfolio Engine</h1>
                <p style="margin:8px 0 0 0; color:#8b949e;">Automated Developer Portfolio Hub for {username}</p>
            </div>
            <div style="background:#161b22; border:1px solid #30363d; padding:12px; border-radius:8px; font-family:monospace; font-size:12px; color:#ffb454;">
                🔒 Verified Matrix Core Layer Active
            </div>
        </header>

        <section style="margin-bottom:50px;">
            <h2 style="color:#fff; border-bottom:1px solid #21262d; padding-bottom:10px; font-size:1.5rem;">🌟 Featured Streamlit Projects</h2>
            <div style="margin-top:20px;">{featured_html}</div>
        </section>

        <section style="margin-bottom:50px;">
            <h2 style="color:#fff; border-bottom:1px solid #21262d; padding-bottom:10px; font-size:1.5rem;">📁 Core Tracked Repositories</h2>
            <div class="grid-layout">{tracked_html}</div>
        </section>

        <section style="margin-bottom:40px;">
            <h2 style="color:#fff; border-bottom:1px solid #21262d; padding-bottom:10px; font-size:1.3rem;">📁 Additional Repository Architecture Matrix</h2>
            <div class="matrix-grid">{unassigned_html}</div>
        </section>
    </div>
</body>
</html>"""

    # Keep writing locally on server disk to maintain tree file integrity
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(full_html_output)
        
    # Return raw text safely to prevent data string blocks from getting cropped
    return full_html_output
