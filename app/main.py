from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import cv2
import numpy as np
from PIL import Image
import io
import os
from app.color_analysis import analyze_skin_tone, suggest_colors, change_skin_tone

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    skin_tone = analyze_skin_tone(img)
    color_suggestions = suggest_colors(skin_tone)
    
    return {"skin_tone": skin_tone, "color_suggestions": color_suggestions}

@app.post("/change-skin-tone")
async def change_skin_tone_endpoint(file: UploadFile = File(...), new_tone: str = "light"):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    changed_img = change_skin_tone(img, new_tone)
    
    # Convert the image back to bytes
    is_success, buffer = cv2.imencode(".png", changed_img)
    io_buf = io.BytesIO(buffer)
    
    return {"changed_image": io_buf.getvalue()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)