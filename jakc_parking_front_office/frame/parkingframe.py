import base64
import logging
import os
import wx
from datetime import datetime

from device.printer_device import Printer_device
from device.webcam_device import Webcam_device
from dialog.barcodedialog import Parking_BarcodeDialog
from dialog.carddialog import Parking_CardDialog
from dialog.driverlistdialog import Parking_DriverListDialog
from dialog.missingticketdialog import Parking_MissingDialog
from dialog.pricingdialog import Parking_PricingDialog
from template.parkingclient import ParkingFrame
from db.Db import db

_logger = logging.getLogger(__name__)

class Parking_ClientFrame(ParkingFrame):

	def __init__(self,login_frame):
		#Init View
		ParkingFrame.__init__(self,login_frame)
		self.parent = login_frame		
		self.password = self.parent.password	
		self.booth = self.parent.booth
		self.config = self.parent.config
		self.park_openerp = self.parent.park_openerp
		self.session_id = self.parent.session_id

		#Connect Parking Application
		self.dbconn = db('172.16.0.23', 'parkir', 'postgres', 'pelang1')

		#Fill Logo
		self.fill_logo()
									
		#Init Operator Info
		self.setup_operator_info()								
		
		#Init Session Info
		self.setup_session_info()
		
		#Flag
		#self.capture_image = False
		self.entry_capture = False
		self.exit_capture = False
		
		#Init State
		self.STATE = 'draft'		
		
		self.VEHICLE_CAMERA_STATE = False
		self.DRIVER_CAMERA_STATE = False
		self.PRINTER_STATE = False
				
		self.TRANS_STATE = False
		self.PRICING_STATE = 'none'
		self.DRIVER_STATE = 'none'
		self.CARD_STATE = 'none'
		self.PINALTY_STATE = 'none'
		
		#Init Printer
		#from escpos import *
		#""" Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
		#Epson = printer.Usb(0x04b8,0x0202)  
		# Print text
		#Epson.text("Hello World\n") 
		# Print image
		#Epson.image("logo.gif") 
		# Print QR Code
		#Epson.qr("You can readme from your smartphone")
		# Print barcode
		#Epson.barcode('1324354657687','EAN13',64,2,'','')
		# Cut paper
		#Epson.cut()
		#self.Printer = Printer_device(self, None, '/dev/ttyUSB0', 0)
		#self.printer_status = False		
		#self.Printer = Printer_device(self, ip_address='172.16.0.112', printer_type=1)
		#self.printer_status, self.printer_message = self.Printer.connect()
	 	#if self.printer_status:	 		
	 	#	print self.printer_message
	 	#else:	 		
		#	print self.printer_message
		
							
		#Fill Parking Frame Information
		self.label_operator.SetLabel(str(self.parent.username))
		self.label_company.SetLabel(self.parent.company)
		self.label_booth.SetLabel(self.parent.booth['name'])
		if self.parent.booth['booth_type'] == '0':
			self.label_type.SetLabel('In')	
		if self.parent.booth['booth_type'] == '1':
			self.label_type.SetLabel('Out')
		if self.parent.booth['booth_type'] == '2':
			self.label_type.SetLabel('In / Out')								
		self.label_datetime.SetLabel(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
		
		#Init Camera
		self.init_camera()
		
		#Init Printer
		self.init_printer()		
		
		
		self.clear_vehicle_entry_image()
		self.clear_vehicle_exit_image()
		self.clear_driver_entry_image()
		self.clear_driver_exit_image()

		self.text_car_or_rfid.SetFocus()
	
	def init_camera(self):
		booth_cameras = self.park_openerp.get_booth_cameras(self.booth['id'])[0]		
		if booth_cameras:		
			for booth_camera in booth_cameras:
				if booth_camera['camera_state']  == 'enable':
					if booth_camera['camera_type'] == 'local':
						
						if booth_camera['camera_position'].strip() == '0':						
							self.VEHICLE_CAMERA_STATE = True
							self.vehicle_image_file_path = os.getcwd() + '/capture/vehicle_camera.jpg'
							self.vehicle_camera = Webcam_device(self, 0, self.vehicle_image_file_path , self.panel_camera_01)
																
						if booth_camera['camera_position'].strip() == '1' :
							self.DRIVER_CAMERA_STATE = True
							self.driver_image_file_path = os.getcwd() + '/capture/driver_camera.jpg'
							self.driver_camera = Webcam_device(self, 1, self.driver_image_file_path , self.panel_camera_02)									
		else:
			print "No Camera"
		
	def init_printer(self):
		if self.booth['printer_state'] == 'enable':
			printer_type = self.booth['printer_type']
			if printer_type:		
				if printer_type == 'local':				
					self.Printer = Printer_device(self, None, self.booth['printer_port'], 0)
					connect, message = self.Printer.connect()
					if connect:
						self.PRINTER_STATE = True	
				if printer_type == 'network':
					connect, message = self.Printer = Printer_device(self, self.booth['printer_ip'], self.booth['printer_ip_port'], 1)
					if connect:
						self.PRINTER_STATE = True
			else:
				print "No Printer"
		else:
			print "No Printer"
	
	def setup_operator_info(self):		
		operator, message = self.park_openerp.get_operator_by_uid()
		if operator:							
			self.operator = operator
			self.operator_id = operator['id']
		else:
			dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
			dial.ShowModal()				
		
	def setup_session_info(self):
		if self.session_id:
			session, message = self.park_openerp.get_session(self.session_id)
			if session:
				self.label_session.SetLabel(session['name'])
			else:
				dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()				
		
	def fill_logo(self):
		self.company = 'Jakc Labs'				
		self.filepath = 'images/logo.png'
		img = wx.Image(self.filepath, wx.BITMAP_TYPE_ANY)
		SizeX, SizeY = self.bitmap_logo.GetSize()
		img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
		self.bitmap_logo.SetBitmap(wx.BitmapFromImage(img))							
		
	def refresh_datetime(self,event):
		self.label_datetime.SetLabel(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
		
	def ucase_text(self,event):
		selection = self.text_car_or_rfid.GetSelection()
		value = self.text_car_or_rfid.GetValue().upper()
		self.text_car_or_rfid.ChangeValue(value)
		self.text_car_or_rfid.SetSelection(*selection)		
		
	def upload_image(self, name, trans_id, file_name, file_path, binary_field):
		model = 'ir.attachment'
		with open(file_path, "rb") as image_file:
			datas = base64.b64encode(image_file.read())				
		values = {}
		values.update({'name':name})
		values.update({'res_id': trans_id})
		values.update({'res_model':'parking.transaction'})
		values.update({'trans_id': trans_id})
		values.update({'binary_field': binary_field})
		values.update({'datas_fname': file_name})			
		values.update({'datas':datas})			
		result = self.sock_object.execute(self.parent.dbname, self.parent.uid, self.parent.password, model, 'create', values)
		return result
		
	def process_steps(self,event):
		#Get Keycode From Keyboard		
		x = event.GetKeyCode()						
		if x == wx.WXK_F4: #Back to Login
			self.parent.Show(True)
			self.Destroy()

		#Print Last Receipt
		elif x == wx.WXK_F5:
			if not self.TRANS_STATE:
				dial = wx.MessageDialog(None, 'Are you sure to re-print last transaction receipt ?', 'Warning', wx.YES_NO | wx.ICON_WARNING)
				result = dial.ShowModal()
				if result == wx.ID_YES:
					self.re_print_receipt()
			else:
				dial = wx.MessageDialog(None, 'Release current transaction to re-print receipt!', 'Error', wx.OK | wx.ICON_ERROR)
				dial.ShowModal()

		elif x == wx.WXK_F6:
			if not self.TRANS_STATE:
				if self.text_car_or_rfid.GetValue():
					if self.booth['is_card'] == True:
						self.carddialog = Parking_CardDialog(self)
						self.carddialog.ShowModal()
						if self.card:
							result_rfid, message_rfid = self.park_openerp.rfid_find_vehicle(self.text_car_or_rfid.GetValue())
							if result_rfid:
								if result_rfid['state'] == 'entry':
									values = {}
									values.update({'state': 'rfid'})
									values.update({'card': self.card})
									rfid_update_status, message = self.park_openerp.update_rfid_transaction(result_rfid['id'], values)
									if rfid_update_status:
										dial = wx.MessageDialog(None, 'Valet Transaction Updated', 'Error', wx.OK | wx.ICON_INFORMATION)
										result = dial.ShowModal()
										self.text_car_or_rfid.SetValue("")
									else:
										dial = wx.MessageDialog(None, 'Valet Transaction Update Failed', 'Error', wx.OK | wx.ICON_ERROR)
										result = dial.ShowModal()
								elif result_rfid['state'] == 'exit':
									result_parking, message_parking = self.dbconn.find_transaksi_parkir(result_rfid['card'], result_rfid['plat_number'])
									if result_parking:
										values = {}
										values.update({'state': 'rfid'})
										values.update({'card': self.card})
										rfid_update_status, message = self.park_openerp.update_rfid_transaction(result_rfid['id'], values)
										if rfid_update_status:
											result_rfid_charging, message = self.park_openerp.get_parking_transaction_charging(result_rfid['id'])
											if result_rfid_charging:
												print result_rfid_charging
												result_update, message = self.dbconn.update_transaksi_parkir(result_rfid['card'], result_rfid['plat_number'], result_rfid_charging['total_charging'])
												if result_update:
													self.text_car_or_rfid.SetValue("")
													dial = wx.MessageDialog(None, 'Parking Transaction Updated', 'Error',
																		wx.OK | wx.ICON_INFORMATION)
													dial.Center()
													dial.ShowModal()
												else:
													dial = wx.MessageDialog(None, 'Parking Transaction Update Failed',
																		'Error',
																		wx.OK | wx.ICON_ERROR)
													dial.Center()
													dial.ShowModal()
											else:
												dial = wx.MessageDialog(None, 'Update Transaksi Parkir Error', 'Error',wx.OK | wx.ICON_ERROR)
                                                                                        	dial.Center()
                                                                                        	dial.ShowModal()

										else:
											dial = wx.MessageDialog(None, 'Valet Transaction Update Failed', 'Error',
													wx.OK | wx.ICON_ERROR)
											dial.Center()
											dial.ShowModal()
									else:
										dial = wx.MessageDialog(None, 'Parking Transaction not found', 'Error', wx.OK | wx.ICON_ERROR)
										dial.Center()
										dial.ShowModal()
								else:
									dial = wx.MessageDialog(None, '2 Valet Transaction not Found', 'Error',
															wx.OK | wx.ICON_ERROR)
									dial.Center()
									dial.ShowModal()

							else:
								dial = wx.MessageDialog(None, '1 Valet Transaction not found', 'Error',
														wx.OK | wx.ICON_ERROR)
								dial.Center()
								dial.ShowModal()


		#Process Parking Transaction
		elif x == wx.WXK_RETURN:

			#Clear View TRANS_STATE = TRUE
			if self.TRANS_STATE:
				print "Reset View"
				self.TRANS_STATE = False						
				self.clear_vehicle_entry_image()
				self.clear_vehicle_exit_image()
				self.clear_driver_exit_image()
				self.clear_driver_exit_image()
				self.clear_total_amount()
				self.text_car_or_rfid.SetValue("")
			else:
				if len(self.text_car_or_rfid.GetValue()) > 0:				
					result, message = self.park_openerp.find_vehicle(self.text_car_or_rfid.GetValue())
					#Vechicle Exist
					if result:
						if self.booth['booth_type'] == '0': #Entry Only Booth
							print 'Car Exist and Stop transaction'
							dial = wx.MessageDialog(None, 'Car Exist in Parking Area!', 'Error', wx.OK | wx.ICON_ERROR)
							dial.Center()
							dial.ShowModal()
							self.text_car_or_rfid.SetValue("")
													
						elif self.booth['booth_type'] == '1': #Exit Only Booth
							print 'Car Exist and Continue for exit'								
							self.fill_entry_image(result['attach_ids'])
							result, message = self.exit_process(result)			
							if result:
								self.text_car_or_rfid.SetValue("")
							else:
								dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
								dial.Center()
								dial.ShowModal()
								#self.text_car_or_rfid.SetValue("")						
										 																							
						elif self.booth['booth_type'] == '2': #Entry and Exit booth
							print 'Car Exist and Continue for exit'				
							dial = wx.MessageDialog(None, 'Car Exist, Do you want to continue ?', 'Warning', wx.YES_NO | wx.ICON_WARNING)
							dial.Center()
							dial_result = dial.ShowModal()
							if dial_result == wx.ID_YES:	
								self.fill_entry_image(result['attach_ids'])						
								result, message = self.exit_process(result)
								if result:
									self.text_car_or_rfid.SetValue("")
								else:
									dial = wx.MessageDialog(None,  message, 'Error', wx.OK | wx.ICON_ERROR)
									dial.ShowModal()
									#self.text_car_or_rfid.SetValue("")						
					else:			
						#Vehicle Not Exist
						if self.booth['booth_type'] == '0': #Entry Only Booth
							print 'Car Not Exist and Continue Entry Transaction'						
							result = self.entry_process(self.text_car_or_rfid.GetValue())
							if result:
								self.text_car_or_rfid.SetValue("")
							else:
								dial = wx.MessageDialog(None, 'Error Entry', 'Error', wx.OK | wx.ICON_ERROR)
								dial.Center()
								dial.ShowModal()					
								self.text_car_or_rfid.SetValue("")

						elif self.booth['booth_type'] == '1': #Exit Only Booth
							print 'Car Not Exist and Stop Transaction'
							dial = wx.MessageDialog(None, 'Car Not Exist !', 'Error', wx.OK | wx.ICON_ERROR)
							dial.Center()
							dial.ShowModal()
							self.text_car_or_rfid.SetValue("")

						elif self.booth['booth_type'] == '2': #Entry and Exit Booth
							print 'Car Not Exist and Continue for entry'
							print self.text_car_or_rfid.GetValue()
							result, message = self.entry_process(self.text_car_or_rfid.GetValue())
							if result:
								self.text_car_or_rfid.SetValue("")
							else:
								dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
								dial.Center()
								dial.ShowModal()			
								
																																
		elif x == wx.WXK_ESCAPE: #Exit Parking Frame
			if not self.TRANS_STATE:
				if len(self.text_car_or_rfid.GetValue()) > 0:
					self.text_car_or_rfid.SetValue('')				
				else:
					dial = wx.MessageDialog(None, 'Are you sure to leave parking application!', 'Warning', wx.YES_NO | wx.ICON_WARNING)
					dial.Center()
					result = dial.ShowModal()
					if result == wx.ID_YES:										
						self.parent.Show(True)
						self.Destroy()
					
		elif x == wx.WXK_F2:
			#Pinalty
			if not self.TRANS_STATE:
				if len(self.text_car_or_rfid.GetValue()) > 0:
					dial = wx.MessageDialog(None, 'Are you sure to process pinalty transaction!', 'Warning', wx.YES_NO | wx.ICON_WARNING)
					dial.Center()
					result = dial.ShowModal()
					if result == wx.ID_YES:						
						result, message = self.park_openerp.find_vehicle(self.text_car_or_rfid.GetValue())
						if result: #Vechile Exist									
							result, message = self.exit_missing_ticket(result)					
							if result:
								self.text_car_or_rfid.SetValue("")
							else:
								dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
								dial.ShowModal()	
																			
						else:
							self.MISSING_TICKET_VEHICLE = False
							self.missingticketdialog = Parking_MissingDialog(self)
							self.missingticketdialog.ShowModal()
							if self.MISSING_TICKET_STATE == 'confirm':
								result, message = self.entry_missing_ticket_process(self.text_car_or_rfid.GetValue())
								if result:
									self.text_car_or_rfid.SetValue("")
								else:
									dial = wx.MessageDialog(None, message, 'Error', wx.OK | wx.ICON_ERROR)
									dial.ShowModal()	
																			
				else:
					dial = wx.MessageDialog(None, 'To Process Missing Ticket, Please Provide Plat Number !', 'Missing Ticket - Jakc Labs', wx.OK | wx.ICON_WARNING)
					dial.Center()
					dial.ShowModal()
						
		#elif x == wx.WXK_F1:
		#	self.helpdialog = Parking_HelpDialog(self)
		#	self.helpdialog.ShowModal()
		else:			
			if not self.TRANS_STATE:
				event.Skip()			
	
	def selected_pricing(self,event):
		self.text_car_or_rfid.SetFocus()	
		
	def re_print_receipt(self):
		if self.PRINTER_STATE:
			if self.last_trans:
				print self.last_trans['id']
				if self.last_trans['state'] == 'entry':
					self.Printer.print_entry_receipt(self.last_trans)
				if self.last_trans['state'] == 'exit':
					self.Printer.print_exit_reciept(self.last_trans)
								
	def entry_process(self,barcode):								
		values = {}							
		#Process Driver Information		
		if self.booth['is_driver'] == True:
			#Show Driver Dialog
			#self.driverdialog = Parking_DriverDialog(self)
			#self.driverdialog.ShowModal()
			self.driverlistdialog = Parking_DriverListDialog(self)
			self.driverlistdialog.ShowModal()
			if self.DRIVER_STATE == 'confirm':
				values.update({'entry_driver_id': self.driver_id})				
			else:
				self.DRIVER_STATE = 'none'
				return False, "Please Complete Driver Information"		
		else:
			self.DRIVER_STATE = 'confirm'

		#Process Card ID
		if self.booth['is_card'] == True:
			self.carddialog = Parking_CardDialog(self)
			self.carddialog.ShowModal()
			if self.CARD_STATE == 'confirm':
				values.update({'card': self.card})
		else:
			self.CARD_STATE = 'confirm'

		if self.DRIVER_STATE == 'confirm' and self.CARD_STATE == 'confirm':
			self.DRIVER_STATE = 'none'
			values.update({'plat_number':barcode})			
			values.update({'input_method': '1'})
			values.update({'entry_booth_id':self.booth['id']})
			values.update({'entry_operator_id':self.operator_id})			
							
			#create process				
			trans_id, message = self.park_openerp.create_parking_transaction(values)
							
			#Capture Camera
			if trans_id:
				self.TRANS_STATE = True
				result, message = self.park_openerp.get_parking_transaction(trans_id)
				if result:						
					self.last_trans = result
					if self.VEHICLE_CAMERA_STATE: #State True		
						image = self.vehicle_camera.capture_image()
						if image:			
							img = wx.Image(self.vehicle_image_file_path, wx.BITMAP_TYPE_JPEG)						
							SizeX, SizeY = self.bitmap_image_entry_01.GetSize()
							img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
							self.bitmap_image_entry_01.SetBitmap(wx.BitmapFromImage(img))
							
							#Upload Image
							name = result['trans_id']
							file_name = "entry_" + name + ".jpg"
							self.park_openerp.upload_image(name, trans_id, file_name, self.vehicle_image_file_path, 'entry_front_image')
													
					#Print Receipt
					if self.PRINTER_STATE:
						self.Printer.print_entry_receipt(result)
																														
																														
					return True,""
				else:
					return False,"Error"
			else:
				return False, message
							
	def exit_process(self,tp):				
		trans_id = tp['id']		
		values = {}
		
		if self.booth['is_barcode'] == True:
			self.barcodedialog = Parking_BarcodeDialog(self)
			self.barcodedialog.ShowModal()			
			if self.BARCODE_STATE == 'confirm':			
				if self.barcode != tp['barcode']:					
					return False, "Please Complete Barcode Information"
			else:
				return False, "Please Complete Barcode Information"
						
		if self.booth['is_driver'] == True:
			#Show Driver Dialog
			#self.driverdialog = Parking_DriverDialog(self)
			#self.driverdialog.ShowModal()
			self.driverlistdialog = Parking_DriverListDialog(self)
			self.driverlistdialog.ShowModal()
			if self.DRIVER_STATE == 'confirm':
				values.update({'exit_driver_id': self.driver_id})
			if self.DRIVER_STATE == 'none':				
				return False, "Please Complete Driver Information"		
		else:
			self.DRIVER_STATE = 'confirm'
			
		#Show Pricing Dialog					
		pricings = self.park_openerp.get_pricings_by_booth(self.booth['id'])[0]		
		if pricings:	 	
			print pricings
			if len(pricings) > 1:								
				self.pricingdialog = Parking_PricingDialog(self)						
				self.pricingdialog.ShowModal()
			else:
				self.PRICING_STATE = 'confirm'
				self.pricing_id =  pricings[0]['pricing_id'][0]
				
						
		if self.PRICING_STATE == 'confirm':
			values.update({'pricing_id':self.pricing_id})
		
		if self.PRICING_STATE == 'none':			
			return False, "Please Complete Pricing Information"
																
		if self.DRIVER_STATE == 'confirm' and self.PRICING_STATE == 'confirm':
			
			#Clear STATE
			self.DRIVER_STATE = 'none'
			self.PRICING_STATE = 'none'
			
			values.update({'session_id': self.session_id})
			values.update({'exit_booth_id':self.booth['id']})		
			values.update({'exit_operator_id':self.operator_id})			
			values.update({'state':'exit'})					
			 			
			#Write Transaction		
			update, message = self.park_openerp.update_parking_transaction(trans_id, values)			
			if update:						
				self.TRANS_STATE = True																				
				result, message = self.park_openerp.get_parking_transaction(trans_id)					
				if result:																
					self.last_trans = result
					self.label_totalamount.SetLabel('Rp ' + str(result['total_amount']))							
					if self.VEHICLE_CAMERA_STATE:					
						image = self.vehicle_camera.capture_image()
						if image:							
							img = wx.Image(self.vehicle_image_file_path, wx.BITMAP_TYPE_JPEG)
							SizeX, SizeY = self.bitmap_image_exit_01.GetSize()
							img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
							self.bitmap_image_exit_01.SetBitmap(wx.BitmapFromImage(img))
							
							#Upload Image									
							name = result['trans_id']
							file_name = "exit_" + name + ".jpg"
							self.park_openerp.upload_image(name, trans_id, file_name, self.vehicle_image_file_path, 'exit_front_image')
							
							#Open Barrier Gate					
							#self.text_car_or_rfid.SetValue('')
							
					#Print Exit Receipt
					if self.PRINTER_STATE:										
						self.Printer.print_exit_reciept(result)
																
					return True,""
				else:
					return False,"Error"
			else:
				return False, "Error Exit Process"
																		
		return True, ""
					
	def entry_missing_ticket_process(self, barcode):
		
		values = {}
																					
		#Process Driver Information		
		if self.booth['is_driver'] == True:
			#Show Driver Dialog
			#self.driverdialog = Parking_DriverDialog(self)
			#self.driverdialog.ShowModal()
			self.driverlistdialog = Parking_DriverListDialog(self)
			self.driverlistdialog.ShowModal()
		
			if self.DRIVER_STATE == 'confirm':
				values.update({'entry_driver_id': self.driver_id})	
				values.update({'exit_driver_id': self.driver_id})			
			else:
				self.DRIVER_STATE = 'none'
				return False, "Please Complete Driver Information"		
		else:
			self.DRIVER_STATE = 'confirm'		
	
		#Show Pricing Dialog					
		pricings = self.park_openerp.get_pricings_by_booth(self.booth['id'])[0]		
		if pricings:	 	
			print pricings
			if len(pricings) > 1:				
				print pricings
				self.pricingdialog = Parking_PricingDialog(self)						
				self.pricingdialog.ShowModal()
			else:
				self.PRICING_STATE = 'confirm'
				self.pricing_id =  pricings[0]['pricing_id'][0]
				
						
		if self.PRICING_STATE == 'confirm':
			values.update({'pricing_id':self.pricing_id})
		
		if self.PRICING_STATE == 'none':			
			return False, "Please Complete Pricing Information"
	
		if self.DRIVER_STATE == 'confirm' and self.PRICING_STATE == 'confirm':			
			self.DRIVER_STATE = 'none'
			self.PRICING_STATE = 'none'
			
			#Entry Information
			values.update({'plat_number': self.text_car_or_rfid.GetValue().strip()})
			values.update({'session_id': self.session_id})			
			values.update({'entry_booth_id':self.booth['id']})
			values.update({'entry_datetime': self.entry_date_time})			
			values.update({'entry_operator_id':self.operator_id})
			values.update({'state': 'missing'})
							
			#create process				
			trans_id, message = self.park_openerp.create_parking_transaction(values)
			
			#Capture Camera
			if trans_id:
				self.TRANS_STATE = True								
				result, message = self.park_openerp.get_parking_transaction(trans_id)
				if result:						
					self.last_trans = result
					self.label_totalamount.SetLabel('Rp ' + str(result['total_amount']))			
					if self.VEHICLE_CAMERA_STATE:
						image = self.vehicle_camera.capture_image()
						if image:			
							img = wx.Image(self.vehicle_image_file_path, wx.BITMAP_TYPE_JPEG)						
							SizeX, SizeY = self.bitmap_image_entry_01.GetSize()
							img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
							self.bitmap_image_entry_01.SetBitmap(wx.BitmapFromImage(img))						
							
							#Upload Image																											
							name = result['trans_id']
							file_name = "exit_" + name + ".jpg"
							self.park_openerp.upload_image(name, trans_id, file_name, self.vehicle_image_file_path, 'exit_front_image')
												
					#Print Receipt
					if self.PRINTER_STATE:
						self.Printer.print_exit_reciept(result)																	
						
					return True, ""
				else:
					return False, message
			else:
				return False, message		
				
	def exit_missing_ticket(self, tp):
		trans_id = tp['id']		
		values = {}
		if self.parent.booth['is_driver'] == True:
			#Show Driver Dialog
			#self.driverdialog = Parking_DriverDialog(self)
			#self.driverdialog.ShowModal()
			self.driverlistdialog = Parking_DriverListDialog(self)
			self.driverlistdialog.ShowModel()
			if self.DRIVER_STATE == 'confirm':
				values.update({'exit_driver_id': self.driver_id})
			if self.DRIVER_STATE == 'none':				
				return False, "Please Complete Driver Information"		
		else:
			self.DRIVER_STATE = 'confirm'
			
		#Show Pricing Dialog					
		pricings = self.park_openerp.get_pricings_by_booth(self.booth['id'])[0]		
		if pricings:	 	
			print pricings
			if len(pricings) > 1:				
				print pricings
				self.pricingdialog = Parking_PricingDialog(self)						
				self.pricingdialog.ShowModal()
			else:
				self.PRICING_STATE = 'confirm'
				self.pricing_id =  pricings[0]['pricing_id'][0]
				
						
		if self.PRICING_STATE == 'confirm':
			values.update({'pricing_id':self.pricing_id})
		
		if self.PRICING_STATE == 'none':			
			return False, "Please Complete Pricing Information"
																
		if self.DRIVER_STATE == 'confirm' and self.PRICING_STATE == 'confirm':
			
			#Clear STATE
			self.DRIVER_STATE = 'none'
			self.PRICING_STATE = 'none'
			
			values.update({'session_id': self.session_id})
			values.update({'exit_booth_id':self.booth['id']})		
			values.update({'exit_operator_id':self.operator_id})			
			values.update({'state':'missing'})					
			 			
			#Write Transaction		
			result, message = self.park_openerp.update_parking_transaction(trans_id, values)			
			if result:
				self.TRANS_STATE = True
				result, message = self.park_openerp.get_parking_transaction(trans_id)
				if result:		
					self.last_trans = result
					self.label_totalamount.SetLabel('Rp ' + str(result['total_amount']))							
					if self.VEHICLE_CAMERA_STATE:								
						image = self.vehicle_camera.capture_image()
						if image:							
							img = wx.Image(self.vehicle_image_file_path, wx.BITMAP_TYPE_JPEG)
							SizeX, SizeY = self.bitmap_image_exit_01.GetSize()
							img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
							self.bitmap_image_exit_01.SetBitmap(wx.BitmapFromImage(img))								
							
							#Upload Image																																													
							name = result['trans_id']
							file_name = "exit_" + name + ".jpg"
							self.park_openerp.upload_image(name, trans_id, file_name, self.vehicle_image_file_path, 'exit_front_image')
											
					#Print Exit Receipt
					if self.PRINTER_STATE:
						self.Printer.print_exit_reciept(result)
					
					return True, ""
				else:
					return False, message
			else:
				return False, "Error Exit Process"
													
			#Print Receipt
		return True, ""
																							
	def fill_entry_image(self, attach_ids):
		if attach_ids:
			attach_id = attach_ids[0]		
			result, message = self.park_openerp.get_attachment(attach_id)		
			if result:
				fh = open(os.getcwd() + "/images/entry_image.png", "wb")		
				image_str = result['datas']
				fh.write(image_str.decode('base64'))				
				fh.close()				
				filepath = os.getcwd() + '/images/entry_image.png'
				img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
				SizeX, SizeY = self.bitmap_image_entry_01.GetSize()
				img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
				self.bitmap_image_entry_01.SetBitmap(wx.BitmapFromImage(img))		
			
	def clear_total_amount(self):		
		self.label_totalamount.SetLabel("Rp 0.0")
				
	def clear_vehicle_entry_image(self):
		try:			
			img = wx.Image(os.getcwd() + '/images/no_image.png', wx.BITMAP_TYPE_PNG)
			SizeX, SizeY = self.bitmap_image_entry_01.GetSize()
			img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
			self.bitmap_image_entry_01.SetBitmap(wx.BitmapFromImage(img))									
		except:
			print "Error"
	
	def clear_vehicle_exit_image(self):
		try:			
			img = wx.Image(os.getcwd() + '/images/no_image.png', wx.BITMAP_TYPE_PNG)
			SizeX, SizeY = self.bitmap_image_entry_01.GetSize()
			img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
			self.bitmap_image_entry_01.SetBitmap(wx.BitmapFromImage(img))
													
			img = wx.Image(os.getcwd() + '/images/no_image.png', wx.BITMAP_TYPE_PNG)
			SizeX, SizeY = self.bitmap_image_exit_01.GetSize()
			img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
			self.bitmap_image_exit_01.SetBitmap(wx.BitmapFromImage(img))
		except:
			print "Error"									

	def clear_driver_entry_image(self):
		try:			
			img = wx.Image(os.getcwd() + '/images/no_image.png', wx.BITMAP_TYPE_PNG)
			SizeX, SizeY = self.bitmap_image_entry_02.GetSize()
			img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
			self.bitmap_image_entry_02.SetBitmap(wx.BitmapFromImage(img))									
		except:
			print "Error"
	
	def clear_driver_exit_image(self):
		try:			
			img = wx.Image(os.getcwd() + '/images/no_image.png', wx.BITMAP_TYPE_PNG)
			SizeX, SizeY = self.bitmap_image_entry_02.GetSize()
			img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
			self.bitmap_image_entry_02.SetBitmap(wx.BitmapFromImage(img))
													
			img = wx.Image(os.getcwd() + '/images/no_image.png', wx.BITMAP_TYPE_PNG)
			SizeX, SizeY = self.bitmap_image_exit_02.GetSize()
			img = img.Scale(SizeX, SizeY ,wx.IMAGE_QUALITY_HIGH)
			self.bitmap_image_exit_02.SetBitmap(wx.BitmapFromImage(img))
		except:
			print "Error"									
	
