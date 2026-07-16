# share_card_generator.py
import os
import subprocess
from jinja2 import Template

TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "share_card.html")

def generate_share_card_png(date_str, lunar_date, solar_term, one_liner, keywords, daily_rhythm, output_png_path):
    """
    Renders share_card.html using Jinja2 and screenshots it using headless Google Chrome.
    """
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template not found at {TEMPLATE_PATH}")
        
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html_template = f.read()
        
    template = Template(html_template)
    rendered_html = template.render(
        date=date_str,
        lunar_date=lunar_date,
        solar_term=solar_term,
        one_liner=one_liner,
        keywords=keywords,
        daily_rhythm=daily_rhythm
    )
    
    # Save temporary html next to output png
    output_dir = os.path.dirname(output_png_path)
    os.makedirs(output_dir, exist_ok=True)
    
    temp_html_path = os.path.join(output_dir, "temp_share_card.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    # Execute Chrome Headless screenshot
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if not os.path.exists(chrome_path):
        # Fallback search if path is different (though standard is /Applications)
        print("Warning: Google Chrome not found at standard path. PNG generation may fail.")
        return False
        
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--screenshot={output_png_path}",
        "--window-size=1080,1350",
        f"file://{os.path.abspath(temp_html_path)}"
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Clean up temporary html
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        return True
    except subprocess.CalledProcessError as e:
        print("Chrome screenshot failed:", e.stderr.decode('utf-8', errors='ignore'))
        return False

if __name__ == "__main__":
    # Test generation
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_outputs", "test_share_card.png")
    success = generate_share_card_png(
        date_str="2026-07-15",
        lunar_date="二〇二六年六月初二",
        solar_term="小暑",
        one_liner="今日天地運行以【推進】為軸心，能量活躍。",
        keywords=["建立", "擴展", "流動"],
        daily_rhythm="推進",
        output_png_path=out_path
    )
    print("PNG generation success:", success)
