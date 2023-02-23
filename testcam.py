import cv2
cam = cv2.VideoCapture(1)

while cam.isOpened():
    frame = cam.read()
    ret, frame = cam.read()
    if ret == True:
        # frame = cv2.rotate(frame, cv2.ROTATE_180)
        frame = cv2.flip(frame, 0)

        cv2.imshow('Frame',frame)
        
    
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break