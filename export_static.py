# export_static.py
import os
import shutil
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader

from database import get_daily_state, get_all_daily_states
from app import get_or_create_state

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")

def build_static_site():
    print("Building static site for GitHub Pages...")
    
    # 1. Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    today_template = env.get_template("today.html")
    date_template = env.get_template("date.html")
    archive_template = env.get_template("archive.html")
    
    # Create date output subfolder
    static_date_dir = os.path.join(PROJECT_ROOT, "date")
    os.makedirs(static_date_dir, exist_ok=True)
    
    # 2. Get today state & all historical states
    taipei_now = datetime.utcnow() + timedelta(hours=8)
    today_str = taipei_now.strftime("%Y-%m-%d")
    
    # Render Today Page (index.html)
    today_state = get_or_create_state(today_str)
    today_html = today_template.render(state=today_state)
    
    # Replace absolute URLs to make it compatible with relative routing
    today_html = today_html.replace('href="/static/style.css"', 'href="./static/style.css"')
    today_html = today_html.replace('src="/static/app.js"', 'src="./static/app.js"')
    today_html = today_html.replace('href="/archive"', 'href="./archive.html"')
    today_html = today_html.replace('href="/"', 'href="./index.html"')
    today_html = today_html.replace('window.location.href = `/date/${dateInput}`', 'window.location.href = `./date/${dateInput}.html`')
    
    with open(os.path.join(PROJECT_ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(today_html)
    print("  index.html (Created)")
    
    # Render Archive Page (archive.html)
    states = get_all_daily_states()
    archive_html = archive_template.render(states=states)
    archive_html = archive_html.replace('href="/static/style.css"', 'href="./static/style.css"')
    archive_html = archive_html.replace('href="/archive"', 'href="./archive.html"')
    archive_html = archive_html.replace('href="/"', 'href="./index.html"')
    archive_html = archive_html.replace('href="/date/', 'href="./date/')
    # Append .html extension to dates links
    for st in states:
        d = st["date"]
        archive_html = archive_html.replace(f'href="./date/{d}"', f'href="./date/{d}.html"')
        
    with open(os.path.join(PROJECT_ROOT, "archive.html"), "w", encoding="utf-8") as f:
        f.write(archive_html)
    print("  archive.html (Created)")
    
    # Render Date Pages (date/YYYY-MM-DD.html)
    for st in states:
        d_str = st["date"]
        d_state = get_or_create_state(d_str)
        d_html = date_template.render(state=d_state)
        
        # Relative replacements for subfolder
        d_html = d_html.replace('href="/static/style.css"', 'href="../static/style.css"')
        d_html = d_html.replace('src="/static/app.js"', 'src="../app_static_override.js"')
        d_html = d_html.replace('href="/archive"', 'href="../archive.html"')
        d_html = d_html.replace('href="/"', 'href="../index.html"')
        d_html = d_html.replace('fetch("/api/daily/ask"', 'fetch("../api/daily/ask"') # note: static ask will error out, but main UI loads fine
        
        with open(os.path.join(static_date_dir, f"{d_str}.html"), "w", encoding="utf-8") as f:
            f.write(d_html)
        print(f"  date/{d_str}.html (Created)")
        
    # Generate relative override JS for the subfolder to handle search query routing correctly
    override_js = """
function queryDate() {
    const dateInput = document.getElementById("dateQuery").value;
    if (dateInput) {
        window.location.href = `../date/${dateInput}.html`;
    }
}
function toggleAskForm() {
    const form = document.getElementById("askForm");
    const triggerBtn = document.querySelector(".ask-trigger-container button");
    if (form.classList.contains("ask-form-hidden")) {
        form.className = "ask-form-visible";
        triggerBtn.textContent = "隱藏問事面板";
    } else {
        form.className = "ask-form-hidden";
        triggerBtn.textContent = "展開問事面板";
    }
}
// Ask submission is dynamic (only works if FastAPI backend is alive, otherwise logs warning)
async function submitAskQuery() {
    alert("動態問事關聯分析功能僅在本地運行 (FastAPI) 時支援，靜態 GitHub Pages 僅提供今日天時瀏覽。");
}
"""
    with open(os.path.join(PROJECT_ROOT, "app_static_override.js"), "w", encoding="utf-8") as f:
        f.write(override_js)
        
    print("Static site build completed successfully!")

if __name__ == "__main__":
    build_static_site()
