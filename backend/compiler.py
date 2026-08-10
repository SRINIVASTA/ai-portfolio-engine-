# https://github.com 
import os 
import re 
import urllib.request 

def scrape_github_about_website(username, repo_name): 
    """ 
    Google AI Style Scraper Core. 
    Downloads the raw HTML of any public GitHub repository page 
    and searches the HTML source code for any live deployment links. 
    """ 
    try: 
        url = f"https://github.com{username}/{repo_name}" 
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}) 
        with urllib.request.urlopen(req, timeout=5) as response: 
            html_content = response.read().decode('utf-8') 
     
        # Scrape the webpage HTML for any valid streamlit.app domain address 
        html_url_match = re.search(r'([a-zA-Z0-9\-_]+\.streamlit\.app[^\s"\'<>#]*)', html_content) 
        if html_url_match: 
            found_url = html_url_match.group(1).strip().rstrip('.,;) /') 
            return f"https://{found_url}" 
    except Exception as e: 
        pass 
    return None 

def auto_generate_portfolio_index(username, ml_sorted_repos): 
    """ 
    Advanced multi-track portfolio compiler engine. 
    Extracts explicit website configurations or uses an active web scraper to 
    pull live URLs straight from the GitHub About Section if missing in payload arrays.
    
    UPDATED: Completely dynamic unsupervised row track compilation framework. 
    """ 
    clean_user = str(username).strip().strip('/') 
    
    # Adaptive dictionary tracks rows natively instead of static hardcoded string buckets
    dynamic_tracks = {} 
    unassigned_html = "" 
    for repo in ml_sorted_repos: 
        name = repo.get('name', 'Unnamed Asset').strip() 
        lang = repo.get('language', 'Python') 
        desc = repo.get('description', '') 
        
        # Pulls the unsupervised track row generated dynamically by your ML processor
        tag = repo.get('tag', 'General Infrastructure Core Systems') 
     
        homepage_url = repo.get('homepage', '') 
        homepage_url = str(homepage_url).strip() if homepage_url else "" 
     
        if not desc or "no public description" in str(desc).lower(): 
            continue 
     
        desc_str = str(desc).strip() 
        
        # ========================================================================= 
        # 1. DYNAMICALLY EXTRACT LIVE WEBSITE LINK 
        # ========================================================================= 
        live_streamlit_url = None 
        
        # Check 1: Extract from the formal GitHub API homepage metadata property 
        if homepage_url and homepage_url.startswith("http"): 
            live_streamlit_url = homepage_url 
        else: 
            # Check 2: Try parsing text-embedded full or bare domain strings 
            extracted_url_match = re.search(r'(https?://[^\s#]+)', desc_str) 
            loose_domain_match = re.search(r'([a-zA-Z0-9\-_]+\.streamlit\.app[^\s#]*)', desc_str) 
     
            if extracted_url_match: 
                live_streamlit_url = extracted_url_match.group(1).strip().rstrip('.,;) /') 
                desc_str = desc_str.replace(extracted_url_match.group(1), '').strip() 
            elif loose_domain_match: 
                captured_raw_url = loose_domain_match.group(1).strip().rstrip('.,;) /') 
                live_streamlit_url = f"https://{captured_raw_url}" 
                desc_str = desc_str.replace(loose_domain_match.group(1), '').strip() 
                
        # Check 3: LIVE SIDEBAR WEB SCRAPER OVERRIDE 
        if not live_streamlit_url or "github.com" in live_streamlit_url: 
            scraped_link = scrape_github_about_website(clean_user, name) 
            if scraped_link: 
                live_streamlit_url = scraped_link 
            else: 
                # Predictable fallback structure matching standard multi-tenant stream pathings 
                if str(lang).lower() == "python" or "streamlit" in name.lower(): 
                    live_streamlit_url = f"https://streamlit.io{clean_user.lower()}/{name.lower()}/main/app.py" 
                else: 
                    live_streamlit_url = f"https://github.com{clean_user}/{name}" 

        # ========================================================================= 
        # CASE-INSENSITIVE SCRUBBER: SAFELY CLEAN TEXT ROWS 
        # ========================================================================= 
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
        # 2. PARSE REPOSITORY TOPICS DYNAMICALLY 
        # ========================================================================= 
        topics = repo.get('topics', []) 
        if not topics: 
            topics = ["streamlit", "python", "data-science", "machine-learning"] 
     
        topics_html = "".join([f'<span style="background:#21262d; color:#8b949e; border:1px solid #30363d; padding:2px 6px; border-radius:4px; font-size:10px; font-family:monospace; margin-right:5px;">#{t}</span>' for t in topics[:4]]) 
     
        # Visual Component Card Layout HTML Frame
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

        # ========================================================================= 
        # 3. DYNAMIC REPOSITORY ROUTING VIA ML-GENERATED TAG TRACKS
        # ========================================================================= 
        if "core_foundation" in tag or name.lower() == "resume":
            lang_color = "#34d399" if lang == "Python" else "#fbbf24" if lang == "HTML" else "#60a5fa" 
            unassigned_html += f""" 
            <a href="https://github.com{clean_user}/{name}" target="_blank" style="background:rgba(33,38,45,0.4); border:1px solid #30363d; padding:14px; border-radius:10px; text-decoration:none; display:block;"> 
                <div style="color:#fff; font-weight:bold; font-size:13px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{name}</div> 
                <div style="color:{lang_color}; font-size:10px; margin-top:4px; font-family:monospace;">🧬 {lang} Matrix Node</div> 
            </a> 
            """ 
        else:
            # Dynamically aggregate card elements based on their exact cluster track row names
            if tag not in dynamic_tracks:
                dynamic_tracks[tag] = ""
            dynamic_tracks[tag] += card_html

    # ========================================================================= 
    # 4. HOIST AND GENERATE DYNAMIC GRID SECTION COMPONENT ROWS
    # ========================================================================= 
    sections_html = ""
    for track_title, cards_content in dynamic_tracks.items():
        if cards_content:
            sections_html += f"""
            <!-- DYNAMIC ROW SECTION -->
            <section style="margin-bottom:40px;">
                <h2 class="section-title">{track_title}</h2>
                <div class="row-grid">
                    {cards_content}
                </div>
            </section>
            """

    # Assemble HTML Output Document Layout Framework Template
    full_html_output = f"""<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <title>{clean_user} | AI Developer Portfolio</title> 
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
            <div style="background:#161b22; border:1px solid #30363d; padding:12px; border-radius:8px; font-family:monospace; font-size:12px; color:#34d399;">
                🔒 Verified Matrix Core Layer Active 
            </div> 
        </header> 
        
        {sections_html}
        
        {f'<section style="margin-bottom:40px;"><h2 class="section-title" style="font-size:1.2rem;">📦 Additional Repository Matrix Nodes</h2><div class="matrix-grid">{unassigned_html}</div></section>' if unassigned_html else ''} 
    </div> 
</body> 
</html>""" 
 
    # Sync and override the storage index document on disk automatically 
    with open("index.html", "w", encoding="utf-8") as file: 
        file.write(full_html_output) 
 
    return full_html_output 
