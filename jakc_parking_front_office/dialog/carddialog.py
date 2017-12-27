import wx

from template.parkingclient import CardDialog


class Parking_CardDialog(CardDialog):
    
    def __init__(self,parent):        
        CardDialog.__init__(self,parent)
        self.parent = parent    
        self.booth = self.parent.booth
        self.commit = False        
        
        #Init OpenERP Class
        self.park_openerp = self.parent.park_openerp
        
        #Init State        
        self.parent.CARD_STATE = 'none'
    
        #Focus
        self.txt_card.SetFocus()
        
    def Text_Card_OnKeyDown(self, event):
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            if len(self.txt_card.GetValue()) > 0:
                self.parent.CARD_STATE = 'confirm'
                self.parent.card = self.txt_card.GetValue()
                self.Destroy()
            else:
                print "Error"            
                                                                                                                                    
        elif x == wx.WXK_ESCAPE:
            if len(self.txt_card.GetValue()) > 0:
                self.txt_card.SetValue('')
                self.parent.CARD_STATE = 'none'
            else:
                self.txt_card.SetValue('')
                self.parent.CARD_STATE = 'none'
                self.Destroy()                    
                                                
        elif x == wx.WXK_BACK:
            self.txt_card.SetValue('')
            self.parent.CARD_STATE = 'none'
        else:                                                            
            event.Skip()        
                
    

                   
            
