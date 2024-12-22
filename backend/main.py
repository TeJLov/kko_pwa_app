import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "FastAPI работает!"}

# Подключение статики (собранный React в 'frontend/build')
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

@app.get("/api/videos")
async def get_videos():
    return {"videos": ["video1.mp4", "video2.mp4"]}
