import wx

from template.parkingclient import MissingTicketDialog


class Parking_MissingDialog(MissingTicketDialog):
    
    def __init__(self,parent):        
        MissingTicketDialog.__init__(self,parent)
        self.parent = parent    
        self.booth = self.parent.booth
        self.commit = False        
        
        self.parent.MISSING_TICKET_STATE = 'request'
        
        #Init OpenERP Class
        self.park_openerp = self.parent.park_openerp
                
    
    def Text_Day_OnKeyDown(self, event):
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            if len(self.txt_day.GetValue()) > 0:
                self.txt_month.SetFocus()
        
        elif x == wx.WXK_ESCAPE:
            if len(self.txt_day.GetValue()) > 0:                
                self.txt_day.SetValue('')
            else:
                self.parent.MISSING_TICKET_STATE = 'none'
                self.Destroy()        
        else:
            event.Skip()    
            
    def Text_Month_OnKeyDown(self, event):
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            if len(self.txt_month.GetValue()) > 0:
                self.txt_year.SetFocus()
        
        elif x == wx.WXK_ESCAPE:
            self.txt_month.SetValue('')                
            self.txt_day.SetFocus()
                
        else:
            event.Skip()    
        
    def Text_Year_OnKeyDown(self, event):
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            if len(self.txt_year.GetValue()) > 0:
                self.txt_hour.SetFocus()
        
        elif x == wx.WXK_ESCAPE:
            self.txt_year.SetValue('')                
            self.txt_month.SetFocus()
        else:
            event.Skip()    
        
        
    def Text_Hour_OnKeyDown(self, event):
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            if len(self.txt_hour.GetValue()) > 0:
                self.txt_minute.SetFocus()
        
        elif x == wx.WXK_ESCAPE:
            self.txt_hour.SetValue('')                
            self.txt_year.SetFocus()            
        else:
            event.Skip()    
        
           
    def Text_Minute_OnKeyDonw(self, event):
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            if len(self.txt_minute.GetValue()) > 0:
                print "Process Missing Ticket"                
                self.parent.MISSING_TICKET_STATE = 'confirm'
                self.parent.entry_date_time = self.txt_year.GetValue() + "-" + self.txt_month.GetValue() + "-" + self.txt_day.GetValue() + " " + self.txt_hour.GetValue() + ":" + self.txt_minute.GetValue() + ":00"                        
                self.Destroy()
                
        elif x == wx.WXK_ESCAPE:
            self.txt_minute.SetValue('')                
            self.txt_hour.SetFocus()
        else:
            event.Skip()    
        
        
    

                   
            
