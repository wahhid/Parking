import wx

from config.read_config import Read_Config
from dialog.logindialog import Parking_LoginDialog
from frame.manlessframe import Parking_ManlessFrame


class Parking_ClientMain(wx.App):
		
	def OnInit(self):	
		self.logindialog = Parking_LoginDialog(None)
		self.logindialog.Show()
		return True
		
class Parking_ManlessMain(wx.App):
	
	def OnInit(self):
		self.manlessframe = Parking_ManlessFrame(None)
		self.manlessframe.Show()
		return True

config = Read_Config()
if not config.config_status:
	print "Config not found"
	exit()
	
if config.serverip and config.serverport and config.boothtype:
	if config.manless == 1:
		app = Parking_ManlessMain(0)
		app.MainLoop()						
	else:		
		app = Parking_ClientMain(0)		
		app.MainLoop()