import wx

from template.parkingclient import DriverDialog


class Parking_DriverDialog(DriverDialog):
    
    def __init__(self,parent):        
        DriverDialog.__init__(self,parent)
        self.parent = parent    
        self.booth = self.parent.booth
        self.commit = False        
        
        #Init OpenERP Class
        self.park_openerp = self.parent.park_openerp
        
        #Init State        
        self.parent.DRIVER_STATE = 'none'
    
        #Focus
        self.txt_driver.SetFocus()
        
    def Text_Driver_OnKeyDown(self, event):
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            print "Enter"
            if len(self.txt_driver.GetValue()) > 0:
                driver, message = self.park_openerp.get_driver(self.txt_driver.GetValue())                
                if driver:                                      
                    self.parent.DRIVER_STATE = 'confirm'                  
                    self.parent.driver_id = driver['id']                                                            
                    self.Destroy()
                else:
                    dial = wx.MessageDialog(self, "Driver not Found", 'Error', wx.OK | wx.ICON_ERROR)
                    dial.Center()
                    dial.ShowModal()
            else:
                print "Error"            
                                                                                                                                    
        elif x == wx.WXK_ESCAPE:
            if len(self.txt_driver.GetValue()) > 0:
                self.txt_driver.SetValue('')
                self.parent.DRIVER_STATE = 'none'
            else:
                self.txt_driver.SetValue('')
                self.parent.DRIVER_STATE = 'none'
                self.Destroy()                    
                                                
        elif x == wx.WXK_BACK:
            self.txt_driver.SetValue('')
            self.parent.DRIVER_STATE = 'none'
        else:                                                            
            event.Skip()        
                
    

                   
            
