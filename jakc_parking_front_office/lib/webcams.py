import numpy as np
from datetime import datetime

import cv2

"""
An example class of how to implement openCV and how it can communicate with the
wxPython layer.
"""
class WebcamFeed(object):
    
    """ Starts a webcam_device feed """
    def __init__(self, webcam_id=0):
        self.webcam_id = webcam_id
        self.webcam = cv2.VideoCapture(self.webcam_id)
		
    """ Determines if the webcam_device is available """
    def has_webcam(self):
        _, frame = self.webcam.read()
        if(isinstance(frame, np.ndarray)):
            return True
        return False
    
    """ Retrieves a frame from the webcam_device and converts it to an RGB - Image """
    def get_image(self, w=None, h=None):
        _, frame = self.webcam.read()
        if w != None and h != None:
            frame = cv2.resize(frame, (w, h))            
            str_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            x = 10
            y = h - 20
            text_color = (255,0,0)
            cv2.putText(frame, '@Jakc Labs - ' + str_str, (x,y), cv2.FONT_HERSHEY_PLAIN, 1.0, text_color, thickness=1, lineType=cv2.CV_AA)
        #return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    """ Retrieves a frame to get the size """
    def size(self):
        _, frame = self.webcam.read()
        return frame.shape[:2]