import cv2

camera_port = 0
ramp_frames = 1

camera = cv2.VideoCapture(camera_port)

def get_image():
    retval, im = camera.read()
    return im

def detect(path):
    camera_capture = get_image()    
    cv2.imwrite(path, camera_capture)
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('test_image_01.jpg', img);

rects, img = detect("test_image.jpg")
box(rects, img)