import os
import wx

from template.parkingclient import DriverListDialog


class Parking_DriverListDialog(DriverListDialog):
    
    def __init__(self,parent):
        DriverListDialog.__init__(self,parent)     
        self.parent = parent    
        self.booth = self.parent.booth
        self.park_openerp = self.parent.park_openerp
        self.index = 0
        self.commit = False
        
        #Init List        
        self.init_list()
        self.fill_list()
        self.list_driver.Select(0)
        
        #Init OpenERP Class                            
        self.parent.PRICING_STATE = 'none'
        
        #Focus
        self.list_driver.SetFocus()
                
    def init_list(self):
        self.list_driver.InsertColumn(0,"ID", width=100)
        self.list_driver.InsertColumn(1,"Driver Name", width=300)

    def add_line(self, datas):
        line = "Line %s" % self.index
        self.list_driver.InsertStringItem(self.index, str(datas['id']))
        self.list_driver.SetStringItem(self.index, 1, datas['name'])        
        self.index += 1
    
    def fill_list(self):        
        results, message = self.park_openerp.get_active_drivers()
        print results
        if results:
            for result in results:
                self.add_line(result)
                print str(result['id']) + ";" + result['name']
        else:
            print message

    def List_Driver_OnListItemSelected(self, event):        
        self.currentItem = event.m_itemIndex
        print str(self.currentItem)
        id = self.list_driver.GetItemText(self.currentItem,0)
            
    def List_Driver_OnKeyDown(self, event):            
        x = event.GetKeyCode()
        if x == wx.WXK_RETURN:
            print "Key Down"
            self.parent.driver_id = self.list_driver.GetItemText(self.currentItem,0)
            self.parent.DRIVER_STATE = 'confirm'
            self.Destroy()    
        elif x == wx.WXK_ESCAPE:
            self.Destroy()        
        else:
            event.Skip()
            
    def fill_image(self, pricing):
        fh = open(os.getcwd() + "/images/pricing.png", "wb")
        if pricing['image1']:
            image_str = pricing['image1']
            fh.write(image_str.decode('base64'))                
            fh.close()                
            filepath = os.getcwd() + '/images/pricing.png'
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
            SizeX, SizeY = self.image_pricing.GetSize()
            img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
            self.image_pricing.SetBitmap(wx.BitmapFromImage(img))                                
        else:
            filepath = os.getcwd() + '/images/no_image.png'
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
            SizeX, SizeY = self.image_pricing.GetSize()
            img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
            self.image_pricing.SetBitmap(wx.BitmapFromImage(img))                    
        
    def process_pricing(self, pricing_id):        
        pricing, message = self.park_openerp.get_pricing(pricing_id)                
        if pricing:
            #Pricing Found
            self.parent.PRICING_STATE = 'confirm'
            self.parent.pricing_id = pricing['id']
            #Fill Image
            fh = open(os.getcwd() + "/images/pricing.png", "wb")
            if pricing['image1']:
                image_str = pricing['image1']
                fh.write(image_str.decode('base64'))                
                fh.close()                
                filepath = os.getcwd() + '/images/pricing.png'
                img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
                SizeX, SizeY = self.image_pricing.GetSize()
                img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                self.image_pricing.SetBitmap(wx.BitmapFromImage(img))
                                
            else:
                filepath = os.getcwd() + '/images/no_image.png'
                img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
                SizeX, SizeY = self.image_pricing.GetSize()
                img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                self.image_pricing.SetBitmap(wx.BitmapFromImage(img))                
        else:
            #Pricing Not Found
            self.text_pricing_code.SetValue('')
            filepath = os.getcwd() + '/images/pricing_not_found.png'
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
            SizeX, SizeY = self.image_pricing.GetSize()
            img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
            self.image_pricing.SetBitmap(wx.BitmapFromImage(img))
            self.parent.PRICING_STATE = 'none'                
        
            
            
            
