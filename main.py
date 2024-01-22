import os
import shutil
from typing import List

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from processor.AIDetector_pytorch import Detector
import core.main

app = FastAPI()

UPLOAD_FOLDER = "./tmp/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)


class ImageInfo(BaseModel):
    status: int
    image_url: str
    draw_url: str
    image_info: dict


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not (file and allowed_file(file.filename)):
        response = ImageInfo(
            status=0,
            image_url="",
            draw_url="",
            image_info={
                "error": "File type error"
            }
        )
        return response

    src_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(src_path, "wb") as f:
        f.write(file.file.read())
    shutil.copy(src_path, "./tmp/ct")
    image_path = os.path.join("./tmp/ct", file.filename)
    pid, image_info = core.main.c_main(
        image_path,
        app.model,
        file.filename.rsplit(".", 1)[1]
    )
    print(pid, image_info)
    response = ImageInfo(
        status=1,
        image_url=f"http://{host}:{str(port)}/tmp/ct/{pid}",
        draw_url=f"http://{host}:{str(port)}/tmp/draw/{pid}",
        image_info=image_info
    )
    return response


@app.get("/tmp/{file}")
async def show_photo(file: str):
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    image_path = f"tmp/{file}"
    return FileResponse(image_path, media_type="image/png")


if __name__ == "__main__":
    host: str = "localhost"
    port: int = 5003

    base_directory: str = "tmp"
    directories: List[str] = [os.path.join(base_directory, dir_name) for dir_name in [
        "ct", "draw", "uploads"]]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    app.mount("/tmp", StaticFiles(directory="./tmp"), name="tmp")
    app.model = Detector()

    uvicorn.run(app, host=host, port=port, log_level="info")
