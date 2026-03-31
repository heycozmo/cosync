from fastapi import FastAPI
from app.core.router import route_command
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.responses import StreamingResponse
from app.services.llm import stream_llm
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/startup")
def startup():
    # check ollama
    # check anything else later
    return {"status": "ready"}

@app.get("/")
def root():
    return {"message": "cosync is running"}


@app.post("/command")
def command(data: dict):
    user_input = data.get("input", "")
    
    result = route_command(user_input)

    if result["type"] == "llm":
        return StreamingResponse(
            stream_llm(result["input"]),
            media_type="text/plain"
        )

    return result


@app.get("/ui", response_class=HTMLResponse)
def ui():
    html_content = Path("app/templates/index.html").read_text()
    return html_content