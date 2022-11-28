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

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        s = ""
        returnable = ""
        for i, det in enumerate(pred):  # per image
            seen += 1
            
            # p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            # p = Path(p)  # to Path
            # save_path = str(save_dir / p.name)  # im.jpg
            # txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            # s += '%gx%g ' % im.shape[2:]  # print string
            # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            # imc = im0.copy() if save_crop else im0  # for save_crop
            # annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                # print(det)
                # det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im.shape).round()

                # print(det)

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {self.names[int(c)]}{'s' * (n > 1)}, conf: {det[:, 4]} "  # add to string
                
                for i in range(det.shape[0]):
                    returnable += "{} {} {} {}".format(det[i, 0],det[i, 1],abs(det[i, 1] - det[i, 3]),det[i, 4])

        
        # Print time (inference-only)
        # print(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")
        return returnable

        # Print results
        t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
        # print(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *self.imgsz)}' % t)
        

# det = my_detector([416,416])
det = my_detector([224,224])
print("loaded")


cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    r = det.my_detect(frame, 0.3)
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