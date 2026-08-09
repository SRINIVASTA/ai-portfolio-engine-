import os

def auto_generate_portfolio_index(username, ml_sorted_repos):
    """
    Completely intercepts the sync session memory matrices to automatically write
    and overwrite the project's root index.html asset folder instantly.
    """
    # 1. Initialize empty containers for our high-converting design layout blocks
    featured_html = ""
    tracked_html = ""
    unassigned_html = ""
    
    # 2. Iterate through the ML-classified repository list tracking models
    for idx, repo in enumerate(ml_sorted_repos):
        name = repo.get('name', 'Unnamed Asset')
        stars = repo.get('stars', 0)
        lang = repo.get('language', 'Python')
        desc = repo.get('description', 'No public description matrix provided in repository configurations.')
        tag = repo.get('tag', 'general')
        
        # --- FEATURED SPLIT DESIGN (Top 3 items match custom highlight criteria) ---
        if idx < 4 and (tag in ["capital_vantage", "transition_control"] or "streamlit" in name.lower()):
            icon = "📈 💰 🚀" if tag == "capital_vantage" else "📈 📊 🚀" if tag == "transition_control" else "🖼️ ⚡ 🤖"
            label = "GenAI Financial Intelligence" if tag == "capital_vantage" else "AI-Driven BPO Intelligence" if tag == "transition_control" else "Streamlit Application Platform"
            
            featured_html += f"""
                <div class="bg-gray-950/50 border border-gray-800 p-6 rounded-xl shadow-xl hover:border-gray-700 transition-all">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-3">
                        <h3 class="text-xl font-bold text-white flex items-center gap-2 flex-wrap">
                            {icon} {name}: {label}
                        </h3>
                        <a href="https://github.com{username}/{name}" target="_blank" class="text-cyan-400 hover:text-cyan-300 font-semibold text-sm shrink-0">💻 View Source Code ↗</a>
                    </div>
                    <p class="text-gray-300 text-base leading-relaxed">
                        {desc}
                    </p>
                    <div class="mt-4 pt-4 border-t border-gray-900/50 flex gap-3">
                        <a href="https://streamlit.app" target="_blank" class="bg-red-600 hover:bg-red-500 text-white text-xs font-bold px-4 py-2 rounded-lg transition-colors">Launch Live Platform</a>
                    </div>
                </div>
            """
        # --- STANDARD CORE TRACKS (Items 4 through 10 display on grid layouts) ---
        elif idx < 10:
            track_title = "📊 Fintech Asset" if tag == "capital_vantage" else "🛠️ BPO System" if tag == "transition_control" else "📁 Core Track Component"
            badge_color = "bg-red-950 text-red-400 border-red-900/50" if tag == "capital_vantage" else "bg-cyan-950 text-cyan-400 border-cyan-900/50" if tag == "transition_control" else "bg-gray-900 text-gray-400 border-gray-800"
            
            tracked_html += f"""
                <div class="bg-gray-950 border border-gray-800 p-6 rounded-xl flex flex-col justify-between">
                    <div>
                        <div class="flex justify-between items-start mb-2">
                            <h3 class="text-lg font-bold text-white truncate">{name}</h3>
                            <span class="text-xs font-mono px-2 py-0.5 border rounded {badge_color}">{lang}</span>
                        </div>
                        <div class="text-xs text-gray-500 font-mono mb-2">{track_title} | ⭐ Stars: {stars}</div>
                        <p class="text-gray-400 text-sm leading-relaxed mb-4 line-clamp-3">{desc}</p>
                    </div>
                    <div class="border-t border-gray-900 pt-3 flex justify-end text-xs font-mono">
                        <a href="https://github.com{username}/{name}" target="_blank" class="text-cyan-400 hover:text-cyan-300 font-bold">View Repo ↗</a>
                    </div>
                </div>
            """
        # --- MATRIX BOX ENTRIES (All remaining repositories) ---
        else:
            lang_color = "text-emerald-500" if lang == "Python" else "text-amber-500" if lang == "HTML" else "text-blue-400"
            unassigned_html += f"""
                <a href="https://github.com{username}/{name}" target="_blank" class="bg-gray-900/20 p-3.5 border border-gray-800/80 rounded-xl hover:border-gray-700 block transition-all">
                    <div class="text-white truncate font-bold">{name}</div>
                    <div class="{lang_color} text-[10px] mt-1">📝 {lang} Matrix Node</div>
                </a>
            """

    # 3. Assemble full production-ready page markup string structures
    full_html_output = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Portfolio Hub & Production Architecture</title>
    <script src="https://jsdelivr.net"></script>
    <style>
        body {{ background-color: #0d1117; color: #c9d1d9; font-family: ui-sans-serif, system-ui, sans-serif; }}
        .streamlit-container-shell {{ width: 100%; height: 680px; border: none; border-radius: 12px; background: #ffffff; }}
    </style>
</head>
<body class="p-4 md:p-12">
    <div class="max-w-5xl mx-auto">
        <!-- HEADER MODULE -->
        <header class="border-b border-gray-800 pb-8 mb-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
                <h1 class="text-3xl font-extrabold text-white flex items-center gap-3">🚀 AI Portfolio Engine</h1>
                <p class="text-gray-400 mt-2 text-md">Automated Developer Portfolio Hub & Isolated RAG Chatbot</p>
                <div class="mt-4 flex items-center gap-2">
                    <span class="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse"></span>
                    <span class="text-xs font-mono text-emerald-400 bg-emerald-950/40 px-2 py-0.5 border border-emerald-900/60 rounded">✓ Verified Production Architecture Integration Enabled</span>
                </div>
            </div>
            <div class="bg-gray-900/50 border border-gray-800 p-4 rounded-xl font-mono text-xs shadow-lg text-amber-400 font-bold">
                🔒 System Matrix Owner: {username}
            </div>
        </header>

        <!-- STREAMLIT CONTROL PANEL EMBED CORE -->
        <section class="mb-14">
            <h2 class="text-2xl font-bold text-white mb-6 border-b border-gray-800 pb-3">⚡ Active Control Center Interface</h2>
            <div class="bg-gray-950 border border-gray-800 p-4 md:p-6 rounded-2xl shadow-2xl">
                <iframe src="https://streamlit.app" class="streamlit-container-shell"></iframe>
            </div>
        </section>

        <!-- FEATURED BLOCK REGION -->
        <section class="mb-14">
            <h2 class="text-2xl font-bold text-white mb-8 border-b border-gray-800 pb-3">🌟 Featured Streamlit Projects</h2>
            <div class="space-y-8">{featured_html}</div>
        </section>

        <!-- GRID BLOCK REGION -->
        <section class="mb-14">
            <h2 class="text-2xl font-bold text-white mb-6 border-b border-gray-800 pb-3">📁 Core Tracked Repositories</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">{tracked_html}</div>
        </section>

        <!-- ARCHITECTURE LONG TAIL MATRIX SECTION -->
        <section class="mb-12">
            <h2 class="text-xl font-bold text-white mb-6">📁 Additional Repository Architecture Matrix</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">{unassigned_html}</div>
        </section>

        <footer class="text-center text-xs text-gray-600 font-mono border-t border-gray-900 pt-8 mt-12">
            © 2026 AI Portfolio Engine Matrix. Automated Architecture Live Overrides Enabled.
        </footer>
    </div>
</body>
</html>"""

    # 4. WRITE THE OUTPUT DIRECTLY TO YOUR ROOT TREE OVERRIDE FILE PATH
    target_path = os.path.join(os.getcwd(), "index.html")
    with open(target_path, "w", encoding="utf-8") as file:
        file.write(full_html_output)
