import random
import time
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import io
import soundfile as sf

app = FastAPI()

# Setup templates and static folders
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load model
model = None # Dummy placeholder

# Class labels
classes = ['pop', 'metal', 'classical', 'jazz', 'rock', 'disco', 'reggae', 'blues', 'hiphop', 'country']


# -------------------- Helper Function --------------------
import hashlib

def predict_genre_from_file(file: UploadFile, model, classes, target_shape=(150, 150)):
    # Deterministic Mock ML process (Same file = Same result)
    contents = file.file.read()
    time.sleep(1) # simulate processing
    
    # Generate a unique stable index based on the file content
    hash_val = int(hashlib.md5(contents).hexdigest(), 16)
    predicted_index = hash_val % len(classes)
    predicted_genre = classes[predicted_index]
    
    # Generate a stable confidence score between 0.75 and 0.99
    confidence = 0.75 + (hash_val % 25) / 100.0
    
    return predicted_genre, float(confidence)


# -------------------- ROUTES --------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})


@app.post("/predict_genre/")
async def get_genre(request: Request, audio_data: UploadFile = File(...)):
    genre, confidence = predict_genre_from_file(audio_data, model, classes)
    return JSONResponse(content={"predicted_genre": genre, "confidence": round(confidence * 100, 2)})


# -------------------- Run --------------------
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
