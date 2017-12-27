# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov 10 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class LoginDialog
###########################################################################

class LoginDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Login - Parking Client", pos = wx.DefaultPosition, size = wx.Size( 348,325 ), style = wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.Size( -1,-1 ) )
		
		fgSizer1 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )
		
		self.bitmap_logo = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.bitmap_logo, 0, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer10 = wx.FlexGridSizer( 4, 2, 0, 0 )
		fgSizer10.AddGrowableCol( 1 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Username", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer10.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.text_username = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.text_username, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer10.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.text_password = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		fgSizer10.Add( self.text_password, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Booth", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		fgSizer10.Add( self.m_staticText16, 0, wx.ALL, 5 )
		
		self.text_booth = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.text_booth, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer10.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer10, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.text_username.Bind( wx.EVT_KEY_DOWN, self.text_username_key_down )
		self.text_password.Bind( wx.EVT_KEY_DOWN, self.text_password_key_down )
		self.text_booth.Bind( wx.EVT_KEY_DOWN, self.text_booth_key_down )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def text_username_key_down( self, event ):
		event.Skip()
	
	def text_password_key_down( self, event ):
		event.Skip()
	
	def text_booth_key_down( self, event ):
		event.Skip()
	

###########################################################################
## Class ParkingFrame
###########################################################################

class ParkingFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Parking Client", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.ICONIZE|wx.MAXIMIZE|wx.STAY_ON_TOP|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer3 = wx.FlexGridSizer( 5, 1, 0, 0 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.AddGrowableRow( 2 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer28 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer28.AddGrowableCol( 0 )
		fgSizer28.SetFlexibleDirection( wx.BOTH )
		fgSizer28.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer4 = wx.FlexGridSizer( 6, 4, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.AddGrowableCol( 3 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Company", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		self.m_staticText4.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
		
		fgSizer4.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.label_company = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_company.Wrap( -1 )
		self.label_company.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.label_company, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Date & Time", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.label_datetime = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_datetime.Wrap( -1 )
		self.label_datetime.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.label_datetime, 0, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Operator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
		
		fgSizer4.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.label_operator = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_operator.Wrap( -1 )
		self.label_operator.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.label_operator, 0, wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Session", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		self.m_staticText10.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.label_session = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_session.Wrap( -1 )
		self.label_session.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.label_session, 0, wx.ALL, 5 )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"Booth", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		self.m_staticText12.SetFont( wx.Font( 12, 74, 90, 90, False, "Arial" ) )
		
		fgSizer4.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.label_booth = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_booth.Wrap( -1 )
		self.label_booth.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.label_booth, 0, wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		self.m_staticText14.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText14, 0, wx.ALL, 5 )
		
		self.label_type = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_type.Wrap( -1 )
		self.label_type.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.label_type, 0, wx.ALL, 5 )
		
		
		fgSizer28.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		self.bitmap_logo = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 200,75 ), 0 )
		fgSizer28.Add( self.bitmap_logo, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( fgSizer28, 1, wx.EXPAND, 5 )
		
		self.text_car_or_rfid = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,100 ), wx.TE_LEFT )
		self.text_car_or_rfid.SetFont( wx.Font( 60, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer3.Add( self.text_car_or_rfid, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		gSizer2 = wx.GridSizer( 1, 3, 0, 0 )
		
		fgSizer15 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer15.AddGrowableCol( 0 )
		fgSizer15.AddGrowableRow( 0 )
		fgSizer15.AddGrowableRow( 1 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.panel_camera_01 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		fgSizer15.Add( self.panel_camera_01, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		
		gSizer2.Add( fgSizer15, 1, wx.EXPAND, 5 )
		
		fgSizer16 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer16.AddGrowableCol( 0 )
		fgSizer16.AddGrowableRow( 0 )
		fgSizer16.AddGrowableRow( 1 )
		fgSizer16.SetFlexibleDirection( wx.BOTH )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.panel_camera_02 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer16.Add( self.panel_camera_02, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		gSizer2.Add( fgSizer16, 1, wx.EXPAND, 5 )
		
		gSizer4 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.bitmap_image_entry_01 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gSizer4.Add( self.bitmap_image_entry_01, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_image_entry_02 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.bitmap_image_entry_02, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_image_exit_01 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		gSizer4.Add( self.bitmap_image_exit_01, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_image_exit_02 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.bitmap_image_exit_02, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		gSizer2.Add( gSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		
		fgSizer3.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		self.label_totalamount = wx.StaticText( self, wx.ID_ANY, u"Rp 0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_totalamount.Wrap( -1 )
		self.label_totalamount.SetFont( wx.Font( 50, 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer3.Add( self.label_totalamount, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText52 = wx.StaticText( self, wx.ID_ANY, u"F1: Help, Esc: Exit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText52.Wrap( -1 )
		self.m_staticText52.SetFont( wx.Font( 16, 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer3.Add( self.m_staticText52, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer3 )
		self.Layout()
		fgSizer3.Fit( self )
		self.refresh_date = wx.Timer()
		self.refresh_date.SetOwner( self, 1 )
		self.refresh_date.Start( 1000 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.text_car_or_rfid.Bind( wx.EVT_KEY_DOWN, self.process_steps )
		self.text_car_or_rfid.Bind( wx.EVT_TEXT, self.ucase_text )
		self.Bind( wx.EVT_TIMER, self.refresh_datetime, id=1 )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def process_steps( self, event ):
		event.Skip()
	
	def ucase_text( self, event ):
		event.Skip()
	
	def refresh_datetime( self, event ):
		event.Skip()
	

###########################################################################
## Class PricingDialog
###########################################################################

class PricingDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Pricing Dialog - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 727,180 ), style = wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer10 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer10.AddGrowableCol( 0 )
		fgSizer10.AddGrowableRow( 0 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.list_pricing = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		self.list_pricing.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer10.Add( self.list_pricing, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.image_pricing = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 250,-1 ), 0 )
		fgSizer10.Add( self.image_pricing, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.list_pricing.Bind( wx.EVT_KEY_DOWN, self.List_Pricing_OnKeyDown )
		self.list_pricing.Bind( wx.EVT_LIST_ITEM_SELECTED, self.List_Pricing_OnListItemSelected )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def List_Pricing_OnKeyDown( self, event ):
		event.Skip()
	
	def List_Pricing_OnListItemSelected( self, event ):
		event.Skip()
	

###########################################################################
## Class DriverDialog
###########################################################################

class DriverDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Driver Dialog - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 716,163 ), style = wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer15 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer15.AddGrowableCol( 0 )
		fgSizer15.AddGrowableRow( 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText93 = wx.StaticText( self, wx.ID_ANY, u"DRIVER", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )
		self.m_staticText93.SetFont( wx.Font( 30, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer15.Add( self.m_staticText93, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.txt_driver = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CAPITALIZE|wx.TE_CENTRE )
		self.txt_driver.SetFont( wx.Font( 40, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer15.Add( self.txt_driver, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer15 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.txt_driver.Bind( wx.EVT_KEY_DOWN, self.Text_Driver_OnKeyDown )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Text_Driver_OnKeyDown( self, event ):
		event.Skip()
	

###########################################################################
## Class TransDetailDialog
###########################################################################

class TransDetailDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 551,318 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		fgSizer6 = wx.FlexGridSizer( 12, 2, 2, 2 )
		fgSizer6.AddGrowableCol( 1 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.label_carnumber = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_carnumber.Wrap( -1 )
		fgSizer6.Add( self.label_carnumber, 0, wx.ALL, 5 )
		
		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Type", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		fgSizer6.Add( self.m_staticText19, 0, wx.ALL, 5 )
		
		self.label_transtype = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_transtype.Wrap( -1 )
		fgSizer6.Add( self.label_transtype, 0, wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"Entry Booth", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		fgSizer6.Add( self.m_staticText21, 0, wx.ALL, 5 )
		
		self.label_boothin = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_boothin.Wrap( -1 )
		fgSizer6.Add( self.label_boothin, 0, wx.ALL, 5 )
		
		self.m_staticText30 = wx.StaticText( self, wx.ID_ANY, u"Enty Datetime", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText30.Wrap( -1 )
		fgSizer6.Add( self.m_staticText30, 0, wx.ALL, 5 )
		
		self.label_datetimein = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_datetimein.Wrap( -1 )
		fgSizer6.Add( self.label_datetimein, 0, wx.ALL, 5 )
		
		self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, u"Entry Operator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		fgSizer6.Add( self.m_staticText32, 0, wx.ALL, 5 )
		
		self.label_operatorin = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_operatorin.Wrap( -1 )
		fgSizer6.Add( self.label_operatorin, 0, wx.ALL, 5 )
		
		self.m_staticText34 = wx.StaticText( self, wx.ID_ANY, u"Entry Shift", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText34.Wrap( -1 )
		fgSizer6.Add( self.m_staticText34, 0, wx.ALL, 5 )
		
		self.label_shiftin = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shiftin.Wrap( -1 )
		fgSizer6.Add( self.label_shiftin, 0, wx.ALL, 5 )
		
		self.m_staticText36 = wx.StaticText( self, wx.ID_ANY, u"Entry Driver", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText36.Wrap( -1 )
		fgSizer6.Add( self.m_staticText36, 0, wx.ALL, 5 )
		
		self.label_driverin = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_driverin.Wrap( -1 )
		fgSizer6.Add( self.label_driverin, 0, wx.ALL, 5 )
		
		self.m_staticText38 = wx.StaticText( self, wx.ID_ANY, u"Exit Booth", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )
		fgSizer6.Add( self.m_staticText38, 0, wx.ALL, 5 )
		
		self.label_boothout = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_boothout.Wrap( -1 )
		fgSizer6.Add( self.label_boothout, 0, wx.ALL, 5 )
		
		self.m_staticText40 = wx.StaticText( self, wx.ID_ANY, u"Exit Datetime", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		fgSizer6.Add( self.m_staticText40, 0, wx.ALL, 5 )
		
		self.label_datetimeout = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_datetimeout.Wrap( -1 )
		fgSizer6.Add( self.label_datetimeout, 0, wx.ALL, 5 )
		
		self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, u"Exit Operator", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText42.Wrap( -1 )
		fgSizer6.Add( self.m_staticText42, 0, wx.ALL, 5 )
		
		self.label_operatorout = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_operatorout.Wrap( -1 )
		fgSizer6.Add( self.label_operatorout, 0, wx.ALL, 5 )
		
		self.m_staticText44 = wx.StaticText( self, wx.ID_ANY, u"Exit Shift", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText44.Wrap( -1 )
		fgSizer6.Add( self.m_staticText44, 0, wx.ALL, 5 )
		
		self.label_shiftout = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_shiftout.Wrap( -1 )
		fgSizer6.Add( self.label_shiftout, 0, wx.ALL, 5 )
		
		self.m_staticText46 = wx.StaticText( self, wx.ID_ANY, u"Exit Driver", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText46.Wrap( -1 )
		fgSizer6.Add( self.m_staticText46, 0, wx.ALL, 5 )
		
		self.label_driverout = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_driverout.Wrap( -1 )
		fgSizer6.Add( self.label_driverout, 0, wx.ALL, 5 )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Car Number", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		fgSizer6.Add( self.m_staticText17, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		fgSizer8 = wx.FlexGridSizer( 6, 2, 2, 2 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText23 = wx.StaticText( self, wx.ID_ANY, u"Duration", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		fgSizer8.Add( self.m_staticText23, 0, wx.ALL, 5 )
		
		self.label_duration = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_duration.Wrap( -1 )
		fgSizer8.Add( self.label_duration, 0, wx.ALL, 5 )
		
		self.m_staticText25 = wx.StaticText( self, wx.ID_ANY, u"Parking Fee", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		fgSizer8.Add( self.m_staticText25, 0, wx.ALL, 5 )
		
		self.label_parkingfee = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_parkingfee.Wrap( -1 )
		fgSizer8.Add( self.label_parkingfee, 0, wx.ALL, 5 )
		
		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, u"Services Fee", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		fgSizer8.Add( self.m_staticText27, 0, wx.ALL, 5 )
		
		self.label_servicefee = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_servicefee.Wrap( -1 )
		fgSizer8.Add( self.label_servicefee, 0, wx.ALL, 5 )
		
		self.m_staticText48 = wx.StaticText( self, wx.ID_ANY, u"Missing Fee", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText48.Wrap( -1 )
		fgSizer8.Add( self.m_staticText48, 0, wx.ALL, 5 )
		
		self.label_missingfee = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_missingfee.Wrap( -1 )
		fgSizer8.Add( self.label_missingfee, 0, wx.ALL, 5 )
		
		self.m_staticText50 = wx.StaticText( self, wx.ID_ANY, u"Limit Fee", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText50.Wrap( -1 )
		fgSizer8.Add( self.m_staticText50, 0, wx.ALL, 5 )
		
		self.label_limitfee = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_limitfee.Wrap( -1 )
		fgSizer8.Add( self.label_limitfee, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer3.Add( fgSizer8, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class MissingTicketDialog
###########################################################################

class MissingTicketDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Missing Ticket - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 773,67 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer11 = wx.FlexGridSizer( 0, 12, 0, 0 )
		fgSizer11.AddGrowableCol( 1 )
		fgSizer11.AddGrowableCol( 3 )
		fgSizer11.AddGrowableCol( 5 )
		fgSizer11.AddGrowableCol( 7 )
		fgSizer11.AddGrowableCol( 9 )
		fgSizer11.AddGrowableCol( 11 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.lbl_day = wx.StaticText( self, wx.ID_ANY, u"Day", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_day.Wrap( -1 )
		self.lbl_day.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.lbl_day, 0, wx.ALL, 5 )
		
		self.txt_day = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txt_day.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.txt_day, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.lblmonth = wx.StaticText( self, wx.ID_ANY, u"Month", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblmonth.Wrap( -1 )
		self.lblmonth.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.lblmonth, 0, wx.ALL, 5 )
		
		self.txt_month = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txt_month.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.txt_month, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.lbl_year = wx.StaticText( self, wx.ID_ANY, u"Year", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_year.Wrap( -1 )
		self.lbl_year.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.lbl_year, 0, wx.ALL, 5 )
		
		self.txt_year = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txt_year.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.txt_year, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.lbl_hour = wx.StaticText( self, wx.ID_ANY, u"Hour", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_hour.Wrap( -1 )
		self.lbl_hour.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.lbl_hour, 0, wx.ALL, 5 )
		
		self.txt_hour = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txt_hour.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.txt_hour, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.lbl_minute = wx.StaticText( self, wx.ID_ANY, u"Minute", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lbl_minute.Wrap( -1 )
		self.lbl_minute.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.lbl_minute, 0, wx.ALL, 5 )
		
		self.txt_minute = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		self.txt_minute.SetFont( wx.Font( 18, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer11.Add( self.txt_minute, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer11 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.txt_day.Bind( wx.EVT_KEY_DOWN, self.Text_Day_OnKeyDown )
		self.txt_month.Bind( wx.EVT_KEY_DOWN, self.Text_Month_OnKeyDown )
		self.txt_year.Bind( wx.EVT_KEY_DOWN, self.Text_Year_OnKeyDown )
		self.txt_hour.Bind( wx.EVT_KEY_DOWN, self.Text_Hour_OnKeyDown )
		self.txt_minute.Bind( wx.EVT_KEY_DOWN, self.Text_Minute_OnKeyDonw )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Text_Day_OnKeyDown( self, event ):
		event.Skip()
	
	def Text_Month_OnKeyDown( self, event ):
		event.Skip()
	
	def Text_Year_OnKeyDown( self, event ):
		event.Skip()
	
	def Text_Hour_OnKeyDown( self, event ):
		event.Skip()
	
	def Text_Minute_OnKeyDonw( self, event ):
		event.Skip()
	

###########################################################################
## Class ManlessFrame
###########################################################################

class ManlessFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Manless Frame - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 781,496 ), style = wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		fgSizer10 = wx.FlexGridSizer( 3, 1, 0, 0 )
		fgSizer10.AddGrowableCol( 0 )
		fgSizer10.AddGrowableRow( 1 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.bitmap_digit_0 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 100,100 ), 0 )
		bSizer6.Add( self.bitmap_digit_0, 0, wx.ALL, 5 )
		
		self.bitmap_digit_1 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 100,100 ), 0 )
		bSizer6.Add( self.bitmap_digit_1, 0, wx.ALL, 5 )
		
		
		fgSizer10.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		list_activityChoices = []
		self.list_activity = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, list_activityChoices, 0 )
		fgSizer10.Add( self.list_activity, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.text_command = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer10.Add( self.text_command, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer9.Add( fgSizer10, 1, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer16 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer16.AddGrowableCol( 0 )
		fgSizer16.AddGrowableRow( 0 )
		fgSizer16.SetFlexibleDirection( wx.BOTH )
		fgSizer16.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gSizer4 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.panel_camera_01 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer4.Add( self.panel_camera_01, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.panel_camera_02 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gSizer4.Add( self.panel_camera_02, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.bitmap_camera_01 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.bitmap_camera_01, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_camera_02 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.bitmap_camera_02, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer16.Add( gSizer4, 1, wx.EXPAND, 5 )
		
		gSizer3 = wx.GridSizer( 2, 4, 0, 0 )
		
		fgSizer17 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer17.AddGrowableCol( 0 )
		fgSizer17.AddGrowableRow( 1 )
		fgSizer17.SetFlexibleDirection( wx.BOTH )
		fgSizer17.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText85 = wx.StaticText( self, wx.ID_ANY, u"Manless", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText85.Wrap( -1 )
		self.m_staticText85.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer17.Add( self.m_staticText85, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.bitmap_status_01 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer17.Add( self.bitmap_status_01, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer17, 1, wx.EXPAND, 5 )
		
		fgSizer18 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer18.AddGrowableCol( 0 )
		fgSizer18.AddGrowableRow( 1 )
		fgSizer18.SetFlexibleDirection( wx.BOTH )
		fgSizer18.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText86 = wx.StaticText( self, wx.ID_ANY, u"Printer", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText86.Wrap( -1 )
		self.m_staticText86.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer18.Add( self.m_staticText86, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.bitmap_status_02 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer18.Add( self.bitmap_status_02, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer18, 1, wx.EXPAND, 5 )
		
		fgSizer19 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer19.AddGrowableCol( 0 )
		fgSizer19.AddGrowableRow( 1 )
		fgSizer19.SetFlexibleDirection( wx.BOTH )
		fgSizer19.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText93 = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )
		self.m_staticText93.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer19.Add( self.m_staticText93, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.bitmap_status_03 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer19.Add( self.bitmap_status_03, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer19, 1, wx.EXPAND, 5 )
		
		fgSizer23 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer23.SetFlexibleDirection( wx.BOTH )
		fgSizer23.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText88 = wx.StaticText( self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText88.Wrap( -1 )
		self.m_staticText88.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer23.Add( self.m_staticText88, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		self.bitmap_status_04 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer23.Add( self.bitmap_status_04, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer23, 1, wx.EXPAND, 5 )
		
		fgSizer24 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer24.AddGrowableCol( 0 )
		fgSizer24.AddGrowableRow( 1 )
		fgSizer24.SetFlexibleDirection( wx.BOTH )
		fgSizer24.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText89 = wx.StaticText( self, wx.ID_ANY, u"Detected", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText89.Wrap( -1 )
		self.m_staticText89.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer24.Add( self.m_staticText89, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_status_11 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer24.Add( self.bitmap_status_11, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer24, 1, wx.EXPAND, 5 )
		
		fgSizer25 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer25.AddGrowableCol( 0 )
		fgSizer25.AddGrowableRow( 1 )
		fgSizer25.SetFlexibleDirection( wx.BOTH )
		fgSizer25.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText90 = wx.StaticText( self, wx.ID_ANY, u"Process", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText90.Wrap( -1 )
		self.m_staticText90.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer25.Add( self.m_staticText90, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_status_12 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer25.Add( self.bitmap_status_12, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer25, 1, wx.EXPAND, 5 )
		
		fgSizer26 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer26.AddGrowableCol( 0 )
		fgSizer26.AddGrowableRow( 1 )
		fgSizer26.SetFlexibleDirection( wx.BOTH )
		fgSizer26.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText91 = wx.StaticText( self, wx.ID_ANY, u"Waiting", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText91.Wrap( -1 )
		self.m_staticText91.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer26.Add( self.m_staticText91, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_status_13 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer26.Add( self.bitmap_status_13, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer26, 1, wx.EXPAND, 5 )
		
		fgSizer27 = wx.FlexGridSizer( 2, 0, 0, 0 )
		fgSizer27.AddGrowableCol( 0 )
		fgSizer27.AddGrowableRow( 1 )
		fgSizer27.SetFlexibleDirection( wx.BOTH )
		fgSizer27.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText92 = wx.StaticText( self, wx.ID_ANY, u"Ready", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText92.Wrap( -1 )
		self.m_staticText92.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		fgSizer27.Add( self.m_staticText92, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )
		
		self.bitmap_status_14 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 50,50 ), 0 )
		fgSizer27.Add( self.bitmap_status_14, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		gSizer3.Add( fgSizer27, 1, wx.EXPAND, 5 )
		
		
		fgSizer16.Add( gSizer3, 1, wx.EXPAND, 5 )
		
		
		bSizer12.Add( fgSizer16, 1, wx.EXPAND, 5 )
		
		
		bSizer9.Add( bSizer12, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer9 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.text_command.Bind( wx.EVT_KEY_DOWN, self.command_steps )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClose( self, event ):
		event.Skip()
	
	def command_steps( self, event ):
		event.Skip()
	

###########################################################################
## Class HelpDialog
###########################################################################

class HelpDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Help Dialog - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 450,295 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer10 = wx.FlexGridSizer( 10, 4, 0, 0 )
		fgSizer10.AddGrowableCol( 1 )
		fgSizer10.AddGrowableCol( 3 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText53 = wx.StaticText( self, wx.ID_ANY, u"F1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText53.Wrap( -1 )
		fgSizer10.Add( self.m_staticText53, 0, wx.ALL, 5 )
		
		self.m_staticText54 = wx.StaticText( self, wx.ID_ANY, u"Help", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText54.Wrap( -1 )
		fgSizer10.Add( self.m_staticText54, 0, wx.ALL, 5 )
		
		self.m_staticText55 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText55.Wrap( -1 )
		fgSizer10.Add( self.m_staticText55, 0, wx.ALL, 5 )
		
		self.m_staticText56 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText56.Wrap( -1 )
		fgSizer10.Add( self.m_staticText56, 0, wx.ALL, 5 )
		
		self.m_staticText57 = wx.StaticText( self, wx.ID_ANY, u"Esc", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText57.Wrap( -1 )
		fgSizer10.Add( self.m_staticText57, 0, wx.ALL, 5 )
		
		self.m_staticText58 = wx.StaticText( self, wx.ID_ANY, u"Exit / Quit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText58.Wrap( -1 )
		fgSizer10.Add( self.m_staticText58, 0, wx.ALL, 5 )
		
		self.m_staticText59 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText59.Wrap( -1 )
		fgSizer10.Add( self.m_staticText59, 0, wx.ALL, 5 )
		
		self.m_staticText60 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText60.Wrap( -1 )
		fgSizer10.Add( self.m_staticText60, 0, wx.ALL, 5 )
		
		self.m_staticText61 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText61.Wrap( -1 )
		fgSizer10.Add( self.m_staticText61, 0, wx.ALL, 5 )
		
		self.m_staticText62 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText62.Wrap( -1 )
		fgSizer10.Add( self.m_staticText62, 0, wx.ALL, 5 )
		
		self.m_staticText63 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText63.Wrap( -1 )
		fgSizer10.Add( self.m_staticText63, 0, wx.ALL, 5 )
		
		self.m_staticText64 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText64.Wrap( -1 )
		fgSizer10.Add( self.m_staticText64, 0, wx.ALL, 5 )
		
		self.m_staticText65 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText65.Wrap( -1 )
		fgSizer10.Add( self.m_staticText65, 0, wx.ALL, 5 )
		
		self.m_staticText66 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText66.Wrap( -1 )
		fgSizer10.Add( self.m_staticText66, 0, wx.ALL, 5 )
		
		self.m_staticText67 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText67.Wrap( -1 )
		fgSizer10.Add( self.m_staticText67, 0, wx.ALL, 5 )
		
		self.m_staticText68 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText68.Wrap( -1 )
		fgSizer10.Add( self.m_staticText68, 0, wx.ALL, 5 )
		
		self.m_staticText69 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText69.Wrap( -1 )
		fgSizer10.Add( self.m_staticText69, 0, wx.ALL, 5 )
		
		self.m_staticText70 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText70.Wrap( -1 )
		fgSizer10.Add( self.m_staticText70, 0, wx.ALL, 5 )
		
		self.m_staticText71 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		fgSizer10.Add( self.m_staticText71, 0, wx.ALL, 5 )
		
		self.m_staticText72 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText72.Wrap( -1 )
		fgSizer10.Add( self.m_staticText72, 0, wx.ALL, 5 )
		
		self.m_staticText73 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText73.Wrap( -1 )
		fgSizer10.Add( self.m_staticText73, 0, wx.ALL, 5 )
		
		self.m_staticText74 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText74.Wrap( -1 )
		fgSizer10.Add( self.m_staticText74, 0, wx.ALL, 5 )
		
		self.m_staticText75 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText75.Wrap( -1 )
		fgSizer10.Add( self.m_staticText75, 0, wx.ALL, 5 )
		
		self.m_staticText76 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText76.Wrap( -1 )
		fgSizer10.Add( self.m_staticText76, 0, wx.ALL, 5 )
		
		self.m_staticText77 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText77.Wrap( -1 )
		fgSizer10.Add( self.m_staticText77, 0, wx.ALL, 5 )
		
		self.m_staticText78 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText78.Wrap( -1 )
		fgSizer10.Add( self.m_staticText78, 0, wx.ALL, 5 )
		
		self.m_staticText79 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText79.Wrap( -1 )
		fgSizer10.Add( self.m_staticText79, 0, wx.ALL, 5 )
		
		self.m_staticText80 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText80.Wrap( -1 )
		fgSizer10.Add( self.m_staticText80, 0, wx.ALL, 5 )
		
		
		self.SetSizer( fgSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_KEY_DOWN, self.helpdialog_key_down )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def helpdialog_key_down( self, event ):
		event.Skip()
	

###########################################################################
## Class CameraPanel
###########################################################################

class CameraPanel ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 400,320 ), style = wx.TAB_TRAVERSAL )
		
	
	def __del__( self ):
		pass
	

###########################################################################
## Class BarcodeDialog
###########################################################################

class BarcodeDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Barcode Dialog - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 600,180 ), style = 0|wx.NO_BORDER )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer15 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer15.AddGrowableCol( 0 )
		fgSizer15.AddGrowableRow( 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText93 = wx.StaticText( self, wx.ID_ANY, u"BARCODE", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )
		self.m_staticText93.SetFont( wx.Font( 30, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer15.Add( self.m_staticText93, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.txt_barcode = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CAPITALIZE|wx.TE_CENTRE )
		self.txt_barcode.SetFont( wx.Font( 40, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer15.Add( self.txt_barcode, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer15 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.txt_barcode.Bind( wx.EVT_KEY_DOWN, self.Text_Barcode_OnKeyDown )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Text_Barcode_OnKeyDown( self, event ):
		event.Skip()
	

###########################################################################
## Class CardDialog
###########################################################################

class CardDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Card Dialog - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 600,180 ), style = wx.STAY_ON_TOP )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer15 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer15.AddGrowableCol( 0 )
		fgSizer15.AddGrowableRow( 0 )
		fgSizer15.SetFlexibleDirection( wx.BOTH )
		fgSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText93 = wx.StaticText( self, wx.ID_ANY, u"CARD", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText93.Wrap( -1 )
		self.m_staticText93.SetFont( wx.Font( 30, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer15.Add( self.m_staticText93, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.txt_card = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_CAPITALIZE|wx.TE_CENTRE )
		self.txt_card.SetFont( wx.Font( 40, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer15.Add( self.txt_card, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer15 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.txt_card.Bind( wx.EVT_KEY_DOWN, self.Text_Card_OnKeyDown )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def Text_Card_OnKeyDown( self, event ):
		event.Skip()
	

###########################################################################
## Class DriverListDialog
###########################################################################

class DriverListDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Driver List Dialog - Jakc Labs", pos = wx.DefaultPosition, size = wx.Size( 727,306 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer10 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer10.AddGrowableCol( 0 )
		fgSizer10.AddGrowableRow( 0 )
		fgSizer10.SetFlexibleDirection( wx.BOTH )
		fgSizer10.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.list_driver = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		self.list_driver.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer10.Add( self.list_driver, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.image_driver = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( 250,-1 ), 0 )
		fgSizer10.Add( self.image_driver, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer10 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.list_driver.Bind( wx.EVT_KEY_DOWN, self.List_Driver_OnKeyDown )
		self.list_driver.Bind( wx.EVT_LIST_ITEM_SELECTED, self.List_Driver_OnListItemSelected )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def List_Driver_OnKeyDown( self, event ):
		event.Skip()
	
	def List_Driver_OnListItemSelected( self, event ):
		event.Skip()
	

