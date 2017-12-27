import os
import wx

from template.parkingclient import PricingDialog


class Parking_PricingDialog(PricingDialog):
	
	def __init__(self,parent):
		PricingDialog.__init__(self,parent) 	
		self.parent = parent	
		self.booth = self.parent.booth
		self.park_openerp = self.parent.park_openerp
		self.index = 0
		self.commit = False
		
		#Init List		
		self.init_list()
		self.fill_list()
		self.list_pricing.Select(0)
		
		#Init OpenERP Class
							
		self.parent.PRICING_STATE = 'none'
		
		#Focus
		self.list_pricing.SetFocus()
				
	def init_list(self):
		self.list_pricing.InsertColumn(0,"Pricing ID", width=100)
		self.list_pricing.InsertColumn(1,"Pricing Name", width=300)

	def add_line(self, datas):
		line = "Line %s" % self.index
		self.list_pricing.InsertStringItem(self.index, str(datas['pricing_id'][0]))
		self.list_pricing.SetStringItem(self.index, 1, datas['pricing_id'][1])        
		self.index += 1
	
	def fill_list(self):		
		results, message = self.park_openerp.get_pricings_by_booth(self.booth['id'])
		print results
		if results:
			for result in results:
				self.add_line(result)
				print str(result['pricing_id'][0]) + ";" + result['pricing_id'][1]

	def List_Pricing_OnListItemSelected(self, event):		
		self.currentItem = event.m_itemIndex
		print str(self.currentItem)
		pricing_id = self.list_pricing.GetItemText(self.currentItem,0)
		pricing, message = self.park_openerp.get_pricing(pricing_id)
		if pricing:
			self.fill_image(pricing)
			
	def List_Pricing_OnKeyDown(self, event):			
		x = event.GetKeyCode()
		if x == wx.WXK_RETURN:
			print "Key Down"
			self.parent.pricing_id = self.list_pricing.GetItemText(self.currentItem,0)
			self.parent.PRICING_STATE = 'confirm'
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

	def find_pricing(self, event):				
		x = event.GetKeyCode()				
		if x == wx.WXK_RETURN:												
			if self.parent.PRICING_STATE == 'confirm':																		
				self.Destroy()
			if self.parent.PRICING_STATE == 'none':
				self.process_pricing(self.text_pricing_code.Value)
																			
		elif x == wx.WXK_ESCAPE:
			if len(self.text_pricing_code.Value) > 0:
				self.text_pricing_code.SetValue('')
				self.parent.PRICING_STATE = 'none'
			else:
				self.text_pricing_code.SetValue('')
				self.parent.PRICING_STATE = 'none'
				self.Destroy()					
												
		elif x == wx.WXK_BACK:
			self.text_pricing_code.SetValue('')
			self.parent.PRICING_STATE = 'none'
		else:									
			event.Skip()
				
		#if self.parent.PRICING_STATE == 'none':											
		#	self.process_pricing(str(chr(x)))				
		
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
		
			
			
			
