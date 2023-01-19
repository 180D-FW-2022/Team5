import numpy as np
from pathlib import Path
import sys
import os
from PIL import Image
import torch
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.augmentations import (Albumentations, augment_hsv, classify_albumentations, classify_transforms, copy_paste,
                                 cutout, letterbox, mixup, random_perspective)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode


import serial

# Initialize Serial comms
def initialize_serial():
    ser = serial.Serial ("/dev/ttyS0", 9600, timeout=1)    #Open port with baud rate
    print("===== Serial Receiver Initialized =====")
    print(ser)
    return ser

class my_detector():

    def __init__(self, imgsz) -> None:
        weights = "best.pt"
        data = ROOT / 'data/coco128.yaml'
        # Load model
        device= ''
        device = select_device(device)
        self.model = DetectMultiBackend(weights, device=device, dnn=False, data=data, fp16=False)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(imgsz, s=self.stride)  # check image size
        self.history = None

    def my_detect(self, im, conf_thres):
        
        bs = 1
        # Run inference
        self.model.warmup(imgsz=(1 if self.pt or self.model.triton else bs, 3, *self.imgsz))  # warmup
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
        
        with dt[0]:
            im = letterbox(im, self.imgsz, stride=self.stride, auto=True)[0]  # padded resize
            im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
            im = np.ascontiguousarray(im)
            im = torch.from_numpy(im).to(self.model.device)
            im = im.half() if self.model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            # visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = self.model(im, augment=False)#, visualize=visualize)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, 0.45, None, False, max_det=1000)

        pred = pred[0]
        modded_pred = np.zeros((pred.shape[0], 3))
        for i, det in enumerate(pred):
            
            modded_pred[i,0] = det[0]
            modded_pred[i,1] = det[1]
            modded_pred[i,2] = det[1] - det[3]
            
            print(modded_pred[:,2])


    def txToController(self, payload):
        # WARNING: imports are weird so hard-coding this serial transmit
        b = (payload + "\0").encode('utf-8')
        ser.write(b)
        #uart_send.write_str(self.ser, payload) 

# det = my_detector([416,416])
det = my_detector([224,224])
print("loaded")


cap = cv2.VideoCapture(0)
ser = initialize_serial()
while True:
    _, frame = cap.read()
    r = det.my_detect(frame, 0.3)
    if r:
        det.txToController(r)
        
        print(r)
    # cv2.imshow('frame',frame)
    # k = cv2.waitKey(5) & 0xFF
    # if k == 27:
    #     break
# im = cv2.imread("smallstop.png")
# # print(im.shape)
# # print(im.shape)
# det.my_detect(im, 0.2)
# detect.run(weights="runs/train/gun_yolov5s_results/weights/best.pt", imgsz=[416, 416], conf_thres=0.2, source="smallstop.png", nosave=True)