import os
import threading
import time
import wx
from datetime import datetime

from connector.mqtt_connector import MQTT_Connector
from device.manless_device import Manless_device
from device.webcam_device import Webcam_device
from openerp.openerp import Openerp
from template.parkingclient import ManlessFrame

from config.read_config import Read_Config


class Parking_ManlessFrame(ManlessFrame):
    
    def __init__(self, parent):
        #Init View
        ManlessFrame.__init__(self,parent)
        self.parent = parent    
        self.card_detected = False
        #Read Config
        self.read_config()
            
        #init Openerp Conection
        self.init_openerp()            
        
        #Login Openerp
        self.login_openerp()
        
        #Fill Booth Code Image
        self.fill_booth_code_image()
        
        #Fill Status Image
        self.fill_status_image()
        
        #Init Manless
        self.init_manless()
        
        #Init MQTT
        self.init_mqtt()
                                        
        #Init Camera        
        self.image_file_path = os.getcwd() + '/capture/camera01.jpg'
        self.camera01 =  Webcam_device(self, 0, self.image_file_path , self.panel_camera_01)
        
        #self.image_file_path = os.getcwd() + '/capture/camera02.jpg'
        #self.camera02 =  Webcam_device(self, 1, self.image_file_path , self.panel_camera_02)
        
        #Init Printer        
        #self.Printer = Printer_device(self, ip_address='172.16.0.112', printer_type=1)
        #self.printer_status, self.printer_message = self.Printer.connect()
        self.printer_status = False
        #if self.printer_status:             
        #    print self.printer_message
        #else:             
        #    print self.printer_message
                   
        #Text Control Set Focus
        self.text_command.SetFocus()
                                                
    def read_config(self):
        self.config = Read_Config()
        
    def init_openerp(self):
        self.openerp = Openerp(self, self.config.serverip, self.config.serverport, self.config.dbname, self.config.appusername, self.config.apppassword)
    
    def init_mqtt(self):
        if self.config.mqttenable == '1':
            print("Connected To MQTT Server")
            self.mqtt_connector = MQTT_Connector(self.config.mqttserverip, self.config.mqttserverport)            
            self.mqtt_connector.connect()
            self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Connected to MQTT Server")
        
    def login_openerp(self):
        result = self.openerp.auth()
        if result:
            self.uid = result
        else:
            self.uid = False

    def init_manless(self):
        self.manless = Manless_device(self, '/dev/ttyACM0', 9600)
        status, message = self.manless.connect()
        
        if status:
            print("Connected To Manless Embedeed")
            self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Connected to Manless")
            t = threading.Thread(name='manless', target=self.manless_thread)
            t.daemon = True 
            t.start()            
            
            self.manless.ser.write('CNS')
            self.filepath = 'images/button_green_480px.png'              
            img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
            SizeX, SizeY = self.bitmap_status_01.GetSize()
            img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
            self.bitmap_status_01.SetBitmap(wx.BitmapFromImage(img))
        else:
            print("Connect to Manless Embedeed Error")
                            
    def fill_booth_code_image(self):
      
        self.filepath = 'images/' +  self.config.boothcode[0:1] + '_100px.png'
        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_digit_0.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_digit_0.SetBitmap(wx.BitmapFromImage(img))

        self.filepath = 'images/' +  self.config.boothcode[1:2] + '_100px.png'
        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_digit_1.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_digit_1.SetBitmap(wx.BitmapFromImage(img))
                
    def fill_status_image(self):
                    
        self.filepath = 'images/button_red_480px.png'
              
        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_01.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_01.SetBitmap(wx.BitmapFromImage(img))

        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_02.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_02.SetBitmap(wx.BitmapFromImage(img))

        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_03.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_03.SetBitmap(wx.BitmapFromImage(img))

        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_04.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_04.SetBitmap(wx.BitmapFromImage(img))
        
        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_11.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_11.SetBitmap(wx.BitmapFromImage(img))

        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_12.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_12.SetBitmap(wx.BitmapFromImage(img))

        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_13.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_13.SetBitmap(wx.BitmapFromImage(img))

        img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
        SizeX, SizeY = self.bitmap_status_14.GetSize()
        img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
        self.bitmap_status_14.SetBitmap(wx.BitmapFromImage(img))
                                                            
    def manless_thread(self):
        while True:
            data = self.manless.ser.readline()
            if len(data) > 0:
                print data.strip()
                if data.strip() == 'CD': #Car Detected
                    self.card_detected = True
                    self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Car Detected")
                    self.filepath = 'images/button_green_480px.png'
                    img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
                    SizeX, SizeY = self.bitmap_status_11.GetSize()
                    img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                    self.bitmap_status_11.SetBitmap(wx.BitmapFromImage(img))
                    #self.mqtt_connector.send("Car Detected")
                                        
                if data.strip() == 'NCD': #No Car Detected
                    self.card_detected = False                    
                    self.filepath = 'images/button_red_480px.png'
                    img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
                    SizeX, SizeY = self.bitmap_status_11.GetSize()
                    img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                    self.bitmap_status_11.SetBitmap(wx.BitmapFromImage(img))
                    #self.mqtt_connector.send("Car Not Detected")
                    
                if data.strip() == 'WP':
                    self.filepath = 'images/button_green_480px.png'
                    img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
                    SizeX, SizeY = self.bitmap_status_12.GetSize()
                    img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                    self.bitmap_status_12.SetBitmap(wx.BitmapFromImage(img))
                    
                if data.strip() == 'NWP':
                    self.filepath = 'images/button_red_480px.png'
                    img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
                    SizeX, SizeY = self.bitmap_status_12.GetSize()
                    img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                    self.bitmap_status_12.SetBitmap(wx.BitmapFromImage(img))
                                                            
                if data.strip() == 'WE':
                    self.filepath = 'images/button_green_480px.png'
                    img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
                    SizeX, SizeY = self.bitmap_status_13.GetSize()
                    img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                    self.bitmap_status_13.SetBitmap(wx.BitmapFromImage(img))
                    
                if data.strip() == 'NWE':
                    self.filepath = 'images/button_red_480px.png'
                    img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
                    SizeX, SizeY = self.bitmap_status_13.GetSize()
                    img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                    self.bitmap_status_13.SetBitmap(wx.BitmapFromImage(img))
                                                            
                if data.strip() == 'RT':
                    self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Request For Transaction")
                    #time.sleep(2)
                    barcode = self.config.boothcode + datetime.now().strftime('%Y%m%d%H%M%S')
                    self.entry_process(barcode)
                    self.manless.ser.write('RTS')
                    self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Request Ticket Success")                                                
            #time.sleep(0.5)
        
    def command_steps(self, event):    
        #Get Keycode From Keyboard        
        x = event.GetKeyCode()                
        if x == wx.WXK_RETURN:
            print "Card Tap"
            value = self.text_command.Value
            
            if value.upper() == 'RESET':                
                self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Send Command " + self.text_command.Value)            
            else:
                self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Process Member with ID " + self.text_command.Value)
            
            #Clear Text Command
            self.text_command.SetValue('')
            
            if self.card_detected:
                result, message = self.openerp.check_membership(value)        
                if result:                
                    self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "Member with ID " + value + " Valid")
                    self.entry_process(value)
                else:
                    self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + message)
            else:
                self.list_activity.Append(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " : " + "No Car Detected")
        else:
            event.Skip()            

    def entry_process(self,barcode):                        
        model = 'parking.transaction'
        values = {}                                    
        self.DRIVER_STATE = 'confirm'            
        if self.DRIVER_STATE == 'confirm':            
            values.update({'is_manless': True})
            values.update({'plat_number': barcode})
            values.update({'entry_booth_id':1})
            values.update({'entry_shift_id':1})
            values.update({'entry_operator_id':1})                
            
            #create process                            
            result, message = self.openerp.create_parking_transaction(values)            
            if result:
                trans_id = result                        
                #Capture Camera
                image = self.camera01.capture_image()
                if image:            
                    img = wx.Image(self.image_file_path, wx.BITMAP_TYPE_JPEG)
                    SizeX, SizeY = self.bitmap_camera_01.GetSize()
                    img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
                    self.bitmap_camera_01.SetBitmap(wx.BitmapFromImage(img))                        
                
                    #Upload Image
                    result, message = self.openerp.get_parking_transaction(trans_id)
                    if result:
                        trans = result                            
                        name = trans['trans_id']
                        file_name = "entry_" + name + ".jpg"
                        self.openerp.upload_image(name, trans_id, file_name, self.image_file_path, 'entry_front_image')                        
                
                #Print Receipt
                if self.printer_status:
                    self.Printer.print_entry_receipt(trans)        
                
                #Open Barier Gate
                                
                #Clear Image            
                t = threading.Thread(name='clear_image', target=self.clear_entry_image)
                t.start()                                    
                return True, ""
            else:
                return False, "Error Transaction"
        
    
    def clear_entry_image(self):
        try:            
            time.sleep(2)
            img = wx.Image(os.getcwd() + '/images/no_image.png', wx.BITMAP_TYPE_PNG)
            SizeX, SizeY = self.bitmap_camera_01.GetSize()
            img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
            self.bitmap_camera_01.SetBitmap(wx.BitmapFromImage(img)) 
        except:
            print "Error"
            

