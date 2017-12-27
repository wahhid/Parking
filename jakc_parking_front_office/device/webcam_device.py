import wx

from lib.webcams import *


class Webcam_device:
    
    def __init__(self, parent, webcam_id=0, image_path=None, panel_camera=None):
        
        self.parent = parent        
        self.image_path = image_path
        self.panel_camera = panel_camera
        self.webcam_id = webcam_id
        
        #Init Webcam
        self.webcam = WebcamFeed(self.webcam_id)
        if not self.webcam.has_webcam():
            print 'Webcam has not been detected.'
        else:            
            self.timer = wx.Timer(self.parent)
            self.timer.Start(1000./20.)
            self.parent.Bind(wx.EVT_TIMER, self.onUpdate, self.timer)
            self.webcam.updating = False
            
            """ Bind custom paint events """
            self.panel_camera.Bind(wx.EVT_ERASE_BACKGROUND, self.onEraseBackground)              
            self.panel_camera.Bind(wx.EVT_PAINT, self.onPaint)
            
            """ Bind a custom close event (needed for Windows) """
            self.parent.Bind(wx.EVT_CLOSE, self.onClose)
            
            """ App states """
            self.STATE_RUNNING = 1
            self.STATE_CLOSING = 2
            self.state = self.STATE_RUNNING
        
    """ When closing, timer needs to be stopped and frame destroyed """
    def onClose(self, event):
        if not self.state == self.STATE_CLOSING:
            self.state = self.STATE_CLOSING
            self.timer.Stop()            
    
    """ Main Update loop that calls the Paint function """
    def onUpdate(self, event):
        if self.state == self.STATE_RUNNING:
            self.panel_camera.Refresh()
            
    """ Retrieves a new webcam image and paints it onto the frame """
    def onPaint(self, event):        
        fw, fh = self.panel_camera.GetSize()                    
        # Retrieve a scaled image from the opencv model
        self.frame = self.webcam.get_image(fw, fh)            
        h, w = self.frame.shape[:2]
        image = wx.BitmapFromBuffer(w, h, self.frame)         
        # Use Buffered Painting to avoid flickering
        dc = wx.BufferedPaintDC(self.panel_camera)
        dc.DrawBitmap(image, 0, 0)    
                    
    """ Background will never be erased, this avoids flickering """
    def onEraseBackground(self, event):
        return  
    
    def capture_image(self):        
        filepath = self.image_path
        cv2.imwrite(filepath, self.frame)        
        return True            
        
    
    