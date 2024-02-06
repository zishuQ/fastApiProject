from pydantic import BaseModel

class ImageInfo(BaseModel):
    image_url: str
    draw_url: str
    image_info: dict


class YoloParam(BaseModel):
    iou_thres: float
    conf_thres: float


class ChooseModel(BaseModel):
    model: str