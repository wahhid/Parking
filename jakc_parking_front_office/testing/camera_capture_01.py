import wx

import cv2
import cv2.cv as cv


class ShowCapture(wx.Panel):    
    
    def __init__(self, parent, capture, fps=50):
        wx.Panel.__init__(self, parent)

        self.capture = capture
        ret, frame = self.capture.read()
    
        height, width = frame.shape[:2]
        parent.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)


    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")        
        ret, frame = self.capture.read()
        if ret:
            color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)            
            #gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)           
            rects = face_cascade.detectMultiScale(color, 1.3, 5, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
            if len(rects) == 0:
                rects = []
            else:
                rects[:, 2:] += rects[:, :2]            
                for x1, y1, x2, y2 in rects:
                    img = cv2.imread("pororo.jpg")
                    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)                                
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)                
                    
            self.bmp.CopyFromBuffer(img)        
            self.Refresh()


capture = cv2.VideoCapture(0)
capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

app = wx.App()
frame = wx.Frame(None)
cap = ShowCapture(frame, capture)
frame.Show()
app.MainLoop()