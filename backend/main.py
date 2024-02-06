import os
import shutil
from typing import List
from datetime import datetime

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from processor.AIDetector_pytorch import Detector
import core.main
from response.models import ImageInfo, YoloParam, ChooseModel
from mysqlite.sqlite_option import SqliteOption

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


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/modelList")
async def modelList():
    model_list = []
    for file in os.listdir("./weights"):
        if file.endswith(".pt"):
            model_list.append(file)
    return {
        "status": 1,
        "msg": "success",
        "data": {
            "modelList": model_list
        }
    }


@app.post("/chooseModel")
async def chooseModel(chooseModel: ChooseModel):
    app.model.weights = f"./weights/{chooseModel.model}"
    return {
        "status": 1,
        "msg": "choose model success",
        "data": {
            "currentModel": chooseModel.model
        }
    }


@app.post("/updateModel")
async def update_model(yoloParam: YoloParam):
    app.model.iou_thres = yoloParam.iou_thres
    app.model.conf_thres = yoloParam.conf_thres
    return {
        "status": 1,
        "msg": "update model thres success",
        "data": {
            "iou_thres": app.model.iou_thres,
            "conf_thres": app.model.conf_thres
        }
    }


@app.post("/upload")
async def upload_file(images: List[UploadFile] = File(...)):
    path = []
    for image in images:
        contents = await image.read()
        file_path = f"{UPLOAD_FOLDER}/{image.filename}"
        path.append(image.filename)
        with open(file_path, "wb") as f:
            f.write(contents)
    with SqliteOption() as db:
        for filename in path:
            data = {}
            data['LineNo'] = 1
            data['TireName'] = filename
            data['ProduceDate'] = datetime.now()
            db.merge_tire_info(data)
    return {
        "status": 1,
        "msg": "upload success",
        "data": {
            "path": path
        }
    }


@app.get("/tmp/{file}")
async def show_photo(file: str):
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    image_path = f"tmp/{file}"
    print(image_path)
    return FileResponse(image_path, media_type="image/png")


@app.get("/imgInfo/{filename}")
async def image_process(filename: str):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not (os.path.exists(filepath) and allowed_file(filename)):
        response = {
            "status": 0,
            "msg": "File type error or file not found",
            "data": {
                "image_url": "",
                "draw_url": "",
                "image_info": {}
            }
        }
        return response

    src_path = os.path.join(UPLOAD_FOLDER, filename)
    shutil.copy(src_path, "./tmp/ct")
    image_path = os.path.join("./tmp/ct", filename)
    pid, image_info = core.main.c_main(
        image_path,
        app.model,
        filename.rsplit(".", 1)[1]
    )
    tmp_ct_path = f"tmp/ct/{pid}"
    tmp_draw_path = f"tmp/draw/{pid}"
    img_info = ImageInfo(
        image_url=f"http://{str(host)}:{str(port)}/{tmp_ct_path}",
        draw_url=f"http://{str(host)}:{str(port)}/{tmp_draw_path}",
        image_info=image_info
    )
    with SqliteOption() as db:
        data = {}
        data['TireName'] = filename
        data['Info'] = image_info.get('label_counts')
        data['DefectDate'] = datetime.now()
        db.merge_detect_info(data)
    response = {
        "status": 1,
        "msg": "get image info success",
        "data": {
            "image_url": img_info.image_url,
            "draw_url": img_info.draw_url,
            "image_info": img_info.image_info
        }
    }
    return response


@app.get("/tireInfo/{product_line}")
async def tireInfo(product_line: str):
    with SqliteOption() as db:
        db_data = db.select_detect_info(product_line)
    sorted_db_data = sorted(
        db_data, key=lambda x: x[3] if x[3] is not None else datetime.min)
    tire_list = []
    for val in sorted_db_data:
        if val[3] is None:
            continue
        tire = {}
        tire["ProductLine"] = f"{val[0]}号"
        tire["TireName"] = f"{val[1].split('.')[0]}号"
        tire["ProduceDate"] = val[2].strftime("%Y-%m-%d %H:%M:%S")
        tire["DefectDate"] = val[3].strftime("%Y-%m-%d %H:%M:%S")
        tire["Info"] = val[4]
        tire_list.append(tire)
    return {
        "status": 1,
        "msg": "get tire info success",
        "data": {
            "tireList": tire_list
        }
    }


if __name__ == "__main__":
    host: str = "localhost"
    port: int = 5003

    base_directory: str = "tmp"
    directories: List[str] = [
        os.path.join(base_directory, dir_name) for dir_name in ["ct", "draw", "uploads"]
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    app.mount("/tmp", StaticFiles(directory="./tmp"), name="tmp")
    app.model = Detector()
    app.model.iou_thres = 0.17
    app.model.conf_thres = 0.2

    uvicorn.run(app, host=host, port=port, log_level="info")
