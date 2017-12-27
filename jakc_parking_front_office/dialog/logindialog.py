import wx

from frame.parkingframe import Parking_ClientFrame
from lib.park_openerp import park
from template.parkingclient import LoginDialog

from config.read_config import Read_Config


class Parking_LoginDialog(LoginDialog):
	
	def __init__(self,parent):
		
		LoginDialog.__init__(self,parent)			

		#Fill Logo
		self.fill_logo()
		
		#Read Configuration
		self.read_config()
							
	
	def read_config(self):		
		self.config = Read_Config()
			
	def fill_logo(self):
		self.company = 'Jakc Labs'				
		self.filepath = 'images/logo.png'
		img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
		SizeX, SizeY = self.bitmap_logo.GetSize()
		img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
		self.bitmap_logo.SetBitmap(wx.BitmapFromImage(img))		
		self.text_username.SetFocus()
		
	def text_username_key_down(self, event):		
		x = event.GetKeyCode()
		if x == wx.WXK_ESCAPE:
			self.text_username.SetValue('')				

		elif x == wx.WXK_TAB:
			if len(self.text_username.Value) == 0:
				dial = wx.MessageDialog(None, 'Please provide username !', 'Warning - Jakc Labs', wx.OK | wx.ICON_WARNING)
				dial.Center()
				dial.ShowModal()
		
		elif x == wx.WXK_RETURN:
			if len(self.text_username.Value) > 0:
				self.text_password.SetFocus()
			else:
				dial = wx.MessageDialog(None, 'Please provice username !', 'Warning - Jakc Labs', wx.OK | wx.ICON_WARNING)
				dial.Center()
				dial.ShowModal()				
		else:
			event.Skip()
			
	def text_password_key_down(self, event):
		x = event.GetKeyCode()
		if x == wx.WXK_ESCAPE:
			self.text_password.SetValue('')
			self.text_username.SetFocus()
		
		elif x == wx.WXK_TAB:
			if len(self.text_password.Value) == 0:
				dial = wx.MessageDialog(None, 'Please provide password !', 'Warning - Jakc Labs', wx.OK | wx.ICON_WARNING)
				dial.Center()
				dial.ShowModal()
			
		elif x == wx.WXK_RETURN:
			if len(self.text_password.Value) > 0:
				self.text_booth.SetFocus()
			else:
				dial = wx.MessageDialog(None, 'Please provide password !', 'Warning - Jakc Labs', wx.OK | wx.ICON_WARNING)
				dial.Center()
				dial.ShowModal()
				
		else:
			event.Skip()
									
	def text_booth_key_down(self, event):		
		x = event.GetKeyCode()		
		if x == wx.WXK_ESCAPE:
			self.text_booth.SetValue('')
			self.text_password.SetFocus()
		
		elif x == wx.WXK_RETURN:
			if len(self.text_booth.Value) > 0:
				self.username = self.text_username.Value
				self.password = self.text_password.Value																									
				self.login(self.username, self.password)
				if self.connect:					
					self.operator = self.park_openerp.uid									
					self.booth, self.message = self.park_openerp.get_booth_by_booth_code(self.text_booth.Value)					
					if self.booth:		
						print "Booth ID : " + str(self.booth['id'])				
						if not self.booth['is_manless']:
							if self.booth['booth_type'] != '0':
								self.session_id, self.message = self.park_openerp.request_session(self.booth['id'])
								if not self.session_id:
									dial = wx.MessageDialog(None, 'Error Create Session!', 'Error', wx.OK | wx.ICON_ERROR)
									dial.ShowModal()
									return False
							else:
								self.session_id = None
																																
							self.parkingframe = Parking_ClientFrame(self)
							self.parkingframe.Maximize(True)
							self.parkingframe.Show()							
							self._clear()
							self.Hide()
							return True
						else:
							dial = wx.MessageDialog(None, str(self.message) , 'Error', wx.OK | wx.ICON_ERROR)
							dial.Center()
							dial.ShowModal()
							return False							
					else:
						dial = wx.MessageDialog(None, 'Booth not Found' , 'Error', wx.OK | wx.ICON_ERROR)
						dial.Center()
						dial.ShowModal()
						return False
				else:
					dial = wx.MessageDialog(None, 'Username or password or booth was wrong!', 'Error', wx.OK | wx.ICON_ERROR)
					dial.Center()
					dial.ShowModal()
					return False				
			else:
				dial = wx.MessageDialog(None, 'Please provide booth information !', 'Warning - Jakc Labs', wx.OK | wx.ICON_WARNING)
				dial.Center()
				dial.ShowModal()		
		else:
			event.Skip()
			
	def login(self, username, password):
		self.park_openerp = park(self.config.serverip, self.config.serverport, self.config.dbname, username, password)
		self.connect, message = self.park_openerp.auth()
	
	def _clear(self):
		self.text_username.SetValue('')
		self.text_password.SetValue('')
		self.text_booth.SetValue('')
		self.text_username.SetFocus()