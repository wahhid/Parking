import cv2

camera_port = 0
ramp_frames = 1

camera = cv2.VideoCapture(camera_port)

def get_image():
    retval, im = camera.read()
    return im

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


temp = get_image()
print "Taking Image..."
camera_capture = get_image()
file = 'test_image.jpg'
cv2.imwrite(file, camera_capture)

img = cv2.imread('test_image.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
faces = face_cascade.detectMultiScale(gray,1.3,5)
for (x,y,w,h) in faces:
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h,x:x+w]
    #roi_color = img[y:y+h,x:x+w]
    #eyes = eye_cascade.detectMultiScale(roi_gray)
    #for(ex,ey,ew,eh) in eyes:
    #    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imwrite('test_image_01.jpg', img)               
#cv2.imshow('img',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
del(camera)    