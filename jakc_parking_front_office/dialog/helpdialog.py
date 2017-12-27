import wx

from template.parkingclient import HelpDialog


class Parking_HelpDialog(HelpDialog):
    
    def __init__(self,parent):
        HelpDialog.__init__(self,parent)
        self.parent = parent    
        self.booth = parent.booth
        self.commit = False
                                
    def helpdialog_key_down(self, event):
        HelpDialog.helpdialog_key_down(self, event)
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            self.Destroy()
        else:
            event.Skip()
        
 