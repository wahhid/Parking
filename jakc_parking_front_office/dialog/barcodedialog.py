import wx

from template.parkingclient import BarcodeDialog


class Parking_BarcodeDialog(BarcodeDialog):
    
    def __init__(self,parent):        
        BarcodeDialog.__init__(self,parent)
        self.parent = parent    
        self.booth = self.parent.booth
        self.commit = False        
        
        #Init OpenERP Class
        self.park_openerp = self.parent.park_openerp
        
        #Init State        
        self.parent.BARCODE_STATE = 'none'
        
        #Focus
        self.txt_barcode.SetFocus()
        
    def Text_Barcode_OnKeyDown(self, event):
                
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:            
            if len(self.txt_barcode.GetValue()) > 0:
                self.parent.BARCODE_STATE = 'confirm'                  
                self.parent.barcode = self.txt_barcode.GetValue()                                                            
                self.Destroy()
                                                                                                                                    
        elif x == wx.WXK_ESCAPE:
            if len(self.txt_barcode.GetValue()) > 0:
                self.txt_barcode.SetValue('')
                self.parent.BARCODE_STATE = 'none'
            else:
                self.txt_barcode.SetValue('')
                self.parent.BARCODE_STATE = 'none'
                self.Destroy()                    
                                                            
        else:                                                            
            event.Skip()        
                
    

                   
            
