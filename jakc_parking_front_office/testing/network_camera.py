import cv2

vcap = cv2.VideoCapture("rtsp://172.16.0.157/MediaInput/h264")
#vcap = cv2.VideoCapture("rtsp://172.16.0.157:554/out.h264")

while(1):

    ret, frame = vcap.read()
    cv2.imshow('VIDEO', frame)
    cv2.waitKey(1)