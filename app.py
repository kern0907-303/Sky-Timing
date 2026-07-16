# app.py
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
import os

from database import init_db, get_daily_state, get_all_daily_states, save_feedback
from generate_daily_state import run_generation
from timing_calculator import calculate_daily_timing
from semantic_state_engine import compute_semantic_vectors
from daily_interpretation import generate_daily_content, ask_daily_timing_relation
from schemas import GenerateRequest, AskRequest, FeedbackRequest

# Initialize FastAPI App
app = FastAPI(title="欽天監今日天時 MVP")

# Set up directories
current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# Ensure DB is initialized
init_db()

def get_or_create_state(date_str, timezone="Asia/Taipei", city="Taipei"):
    state = get_daily_state(date_str, timezone, city)
    if not state:
        # Auto generate on the fly
        run_generation(date_str, timezone, city)
        state = get_daily_state(date_str, timezone, city)
    
    # Format the vectors dictionary keys for display in template
    vector_labels = {
        "generation": "生成 (建立)",
        "expansion": "擴張 (推動)",
        "stabilization": "穩定 (承載)",
        "circulation": "流動 (對接)",
        "contraction": "收斂 (沉澱)",
        "transformation": "轉換 (調整)",
        "disruption": "瓦解 (破缺)",
        "uncertainty": "不確定 (觀察)"
    }
    
    # Calculate text details for HTML display
    timing = state["raw_timing_data"]
    vectors = state["semantic_vectors"]
    forces = {
        "primary_force": state["primary_force"],
        "secondary_force": state["secondary_force"],
        "constraint_force": state["constraint_force"],
        "inner_contradiction": ""
    }
    
    content = generate_daily_content(date_str, timing, vectors, forces)
    state["content"] = content
    state["formatted_vectors"] = {vector_labels.get(k, k): v for k, v in vectors.items()}
    return state

# 1. HTML Routes
@app.get("/", response_class=HTMLResponse)
def read_today(request: Request):
    # Today date string in local Asia/Taipei
    # Offset by +8 hours from UTC
    taipei_now = datetime.utcnow() + timedelta(hours=8)
    date_str = taipei_now.strftime("%Y-%m-%d")
    state = get_or_create_state(date_str)
    return templates.TemplateResponse(request=request, name="today.html", context={"request": request, "state": state})

@app.get("/date/{date_str}", response_class=HTMLResponse)
def read_date(request: Request, date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    state = get_or_create_state(date_str)
    return templates.TemplateResponse(request=request, name="date.html", context={"request": request, "state": state})

@app.get("/archive", response_class=HTMLResponse)
def read_archive(request: Request):
    states = get_all_daily_states()
    return templates.TemplateResponse(request=request, name="archive.html", context={"request": request, "states": states})

# 2. REST API Routes
@app.get("/api/daily/today")
def api_today():
    taipei_now = datetime.utcnow() + timedelta(hours=8)
    date_str = taipei_now.strftime("%Y-%m-%d")
    return get_or_create_state(date_str)

@app.get("/api/daily/{date_str}")
def api_date(date_str: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    return get_or_create_state(date_str)

@app.post("/api/daily/generate")
def api_generate(req: GenerateRequest):
    try:
        datetime.strptime(req.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    state = get_or_create_state(req.date, req.timezone, req.city)
    return {"status": "success", "state": state}

@app.post("/api/daily/ask")
def api_ask(req: AskRequest):
    state = get_daily_state(req.date)
    if not state:
        state = get_or_create_state(req.date)
        
    forces = {
        "primary_force": state["primary_force"],
        "secondary_force": state["secondary_force"],
        "constraint_force": state["constraint_force"]
    }
    
    # Calculate forces contradiction in the interpret engine
    timing = state["raw_timing_data"]
    vectors = state["semantic_vectors"]
    _, forces_complete = compute_semantic_vectors(timing)
    
    response_text = ask_daily_timing_relation(
        timing, vectors, forces_complete,
        req.question, req.event_type, req.constraint
    )
    return {"status": "success", "response": response_text}

@app.post("/api/daily/feedback")
def api_feedback(req: FeedbackRequest):
    success = save_feedback(
        req.date,
        req.reaction,
        req.observation,
        req.anonymous_session_id
    )
    if not success:
        return {"status": "error", "message": "今天您已經提交過反饋囉。"}
    return {"status": "success", "message": "反饋提交成功，感謝您的觀察！"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
