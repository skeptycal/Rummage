# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class RummageFrame
###########################################################################

class RummageFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Rummage", pos = wx.DefaultPosition, size = wx.Size( 771,520 ), style = wx.DEFAULT_FRAME_STYLE|wx.RESIZE_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		self.SetSizeHintsSz( wx.Size( -1,-1 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bFrameSizer = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer13 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer13.AddGrowableCol( 0 )
		fgSizer13.AddGrowableRow( 0 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_grep_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_settings_panel = wx.Panel( self.m_grep_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 4, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_searchin_panel = wx.Panel( self.m_settings_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_searchin_panel, wx.ID_ANY, u"Search In" ), wx.VERTICAL )
		
		fgSizer121 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer121.AddGrowableCol( 0 )
		fgSizer121.SetFlexibleDirection( wx.BOTH )
		fgSizer121.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		m_searchin_textChoices = []
		self.m_searchin_text = wx.ComboBox( self.m_searchin_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_searchin_textChoices, wx.TE_PROCESS_ENTER|wx.TAB_TRAVERSAL|wx.WANTS_CHARS )
		fgSizer121.Add( self.m_searchin_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_searchin_dir_picker = wx.DirPickerCtrl( self.m_searchin_panel, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer121.Add( self.m_searchin_dir_picker, 1, wx.EXPAND, 5 )
		
		
		sbSizer1.Add( fgSizer121, 1, wx.EXPAND, 5 )
		
		
		self.m_searchin_panel.SetSizer( sbSizer1 )
		self.m_searchin_panel.Layout()
		sbSizer1.Fit( self.m_searchin_panel )
		fgSizer2.Add( self.m_searchin_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_search_panel = wx.Panel( self.m_settings_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_search_panel, wx.ID_ANY, u"Search" ), wx.VERTICAL )
		
		fgSizer6 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer6.AddGrowableCol( 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer7 = wx.FlexGridSizer( 1, 2, 0, 0 )
		fgSizer7.SetFlexibleDirection( wx.BOTH )
		fgSizer7.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_search_regex_radio = wx.RadioButton( self.m_search_panel, wx.ID_ANY, u"Regex Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_search_regex_radio.SetValue( True ) 
		fgSizer7.Add( self.m_search_regex_radio, 0, wx.ALL, 5 )
		
		self.m_search_text_radio = wx.RadioButton( self.m_search_panel, wx.ID_ANY, u"Text Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer7.Add( self.m_search_text_radio, 0, wx.ALL, 5 )
		
		
		fgSizer6.Add( fgSizer7, 1, wx.EXPAND, 5 )
		
		fgSizer8 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer8.AddGrowableCol( 1 )
		fgSizer8.SetFlexibleDirection( wx.BOTH )
		fgSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_searchfor_label = wx.StaticText( self.m_search_panel, wx.ID_ANY, u"Search for:", wx.DefaultPosition, wx.DefaultSize, 0|wx.TAB_TRAVERSAL )
		self.m_searchfor_label.Wrap( -1 )
		fgSizer8.Add( self.m_searchfor_label, 0, wx.ALL, 5 )
		
		m_searchfor_textboxChoices = []
		self.m_searchfor_textbox = wx.ComboBox( self.m_search_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_searchfor_textboxChoices, wx.TE_PROCESS_ENTER|wx.TAB_TRAVERSAL|wx.WANTS_CHARS )
		fgSizer8.Add( self.m_searchfor_textbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer6.Add( fgSizer8, 1, wx.EXPAND, 5 )
		
		fgSizer9 = wx.FlexGridSizer( 2, 3, 0, 0 )
		fgSizer9.SetFlexibleDirection( wx.BOTH )
		fgSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_case_checkbox = wx.CheckBox( self.m_search_panel, wx.ID_ANY, u"Search case-sensitive", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer9.Add( self.m_case_checkbox, 0, wx.ALL, 5 )
		
		self.m_dotmatch_checkbox = wx.CheckBox( self.m_search_panel, wx.ID_ANY, u"Dot matches newline", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer9.Add( self.m_dotmatch_checkbox, 0, wx.ALL, 5 )
		
		self.m_utf8_checkbox = wx.CheckBox( self.m_search_panel, wx.ID_ANY, u"Treat all as UTF-8", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer9.Add( self.m_utf8_checkbox, 0, wx.ALL, 5 )
		
		
		fgSizer6.Add( fgSizer9, 1, wx.EXPAND, 5 )
		
		
		sbSizer2.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		
		self.m_search_panel.SetSizer( sbSizer2 )
		self.m_search_panel.Layout()
		sbSizer2.Fit( self.m_search_panel )
		fgSizer2.Add( self.m_search_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_limiter_panel = wx.Panel( self.m_settings_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self.m_limiter_panel, wx.ID_ANY, u"Limit Search" ), wx.HORIZONTAL )
		
		self.m_limit_size_panel = wx.Panel( self.m_limiter_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer11 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer11.AddGrowableCol( 0 )
		fgSizer11.SetFlexibleDirection( wx.BOTH )
		fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_all_size_radio = wx.RadioButton( self.m_limit_size_panel, wx.ID_ANY, u"All sizes", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_all_size_radio.SetValue( True ) 
		fgSizer11.Add( self.m_all_size_radio, 0, wx.ALL, 5 )
		
		fgSizer12 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer12.AddGrowableCol( 2 )
		fgSizer12.SetFlexibleDirection( wx.BOTH )
		fgSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_size_radio = wx.RadioButton( self.m_limit_size_panel, wx.ID_ANY, u"Size is", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_size_radio, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		m_logic_choiceChoices = [ u"greater than", u"equal to", u"less than" ]
		self.m_logic_choice = wx.Choice( self.m_limit_size_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_logic_choiceChoices, 0 )
		self.m_logic_choice.SetSelection( 0 )
		fgSizer12.Add( self.m_logic_choice, 0, wx.ALL, 5 )
		
		self.m_size_text = wx.TextCtrl( self.m_limit_size_panel, wx.ID_ANY, u"1000", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer12.Add( self.m_size_text, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_size_type_label = wx.StaticText( self.m_limit_size_panel, wx.ID_ANY, u"KB", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_size_type_label.Wrap( -1 )
		fgSizer12.Add( self.m_size_type_label, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer11.Add( fgSizer12, 1, wx.EXPAND, 5 )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_subfolder_checkbox = wx.CheckBox( self.m_limit_size_panel, wx.ID_ANY, u"Include subfolders", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_subfolder_checkbox.SetValue(True) 
		gSizer1.Add( self.m_subfolder_checkbox, 0, wx.ALL, 5 )
		
		self.m_hidden_checkbox = wx.CheckBox( self.m_limit_size_panel, wx.ID_ANY, u"Include hidden", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_hidden_checkbox, 0, wx.ALL, 5 )
		
		
		fgSizer11.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		
		self.m_limit_size_panel.SetSizer( fgSizer11 )
		self.m_limit_size_panel.Layout()
		fgSizer11.Fit( self.m_limit_size_panel )
		sbSizer4.Add( self.m_limit_size_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticline4 = wx.StaticLine( self.m_limiter_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_VERTICAL )
		sbSizer4.Add( self.m_staticline4, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_limit_panel = wx.Panel( self.m_limiter_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer141 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer141.SetFlexibleDirection( wx.BOTH )
		fgSizer141.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_filematchregex_radio = wx.RadioButton( self.m_limit_panel, wx.ID_ANY, u"Regex match", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_filematchregex_radio.SetValue( True ) 
		fgSizer141.Add( self.m_filematchregex_radio, 0, wx.ALL, 5 )
		
		self.m_filematchtext_radio = wx.RadioButton( self.m_limit_panel, wx.ID_ANY, u"Text match", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_filematchtext_radio.SetValue( True ) 
		fgSizer141.Add( self.m_filematchtext_radio, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( fgSizer141, 1, wx.EXPAND, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_exclude_label = wx.StaticText( self.m_limit_panel, wx.ID_ANY, u"Exclude dirs (Regex):", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_exclude_label.Wrap( -1 )
		fgSizer4.Add( self.m_exclude_label, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		m_exclude_textboxChoices = []
		self.m_exclude_textbox = wx.ComboBox( self.m_limit_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_exclude_textboxChoices, wx.TE_PROCESS_ENTER|wx.TAB_TRAVERSAL|wx.WANTS_CHARS )
		fgSizer4.Add( self.m_exclude_textbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_filematch_label = wx.StaticText( self.m_limit_panel, wx.ID_ANY, u"Files which match:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_filematch_label.Wrap( -1 )
		fgSizer4.Add( self.m_filematch_label, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		m_filematch_textboxChoices = []
		self.m_filematch_textbox = wx.ComboBox( self.m_limit_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_filematch_textboxChoices, wx.TE_PROCESS_ENTER|wx.TAB_TRAVERSAL|wx.WANTS_CHARS )
		fgSizer4.Add( self.m_filematch_textbox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer3.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		
		self.m_limit_panel.SetSizer( fgSizer3 )
		self.m_limit_panel.Layout()
		fgSizer3.Fit( self.m_limit_panel )
		sbSizer4.Add( self.m_limit_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_limiter_panel.SetSizer( sbSizer4 )
		self.m_limiter_panel.Layout()
		sbSizer4.Fit( self.m_limiter_panel )
		fgSizer2.Add( self.m_limiter_panel, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_action_panel = wx.Panel( self.m_settings_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bActionSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.m_search_button = wx.Button( self.m_action_panel, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		bActionSizer.Add( self.m_search_button, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		self.m_action_panel.SetSizer( bActionSizer )
		self.m_action_panel.Layout()
		bActionSizer.Fit( self.m_action_panel )
		fgSizer2.Add( self.m_action_panel, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer10.Add( fgSizer2, 0, wx.EXPAND, 5 )
		
		
		self.m_settings_panel.SetSizer( bSizer10 )
		self.m_settings_panel.Layout()
		bSizer10.Fit( self.m_settings_panel )
		self.m_grep_notebook.AddPage( self.m_settings_panel, u"Search", True )
		self.m_result_file_panel = wx.Panel( self.m_grep_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_result_file_list = wx.ListCtrl( self.m_result_file_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer7.Add( self.m_result_file_list, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_result_file_panel.SetSizer( bSizer7 )
		self.m_result_file_panel.Layout()
		bSizer7.Fit( self.m_result_file_panel )
		self.m_grep_notebook.AddPage( self.m_result_file_panel, u"Files", False )
		self.m_result_content_panel = wx.Panel( self.m_grep_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_result_list = wx.ListCtrl( self.m_result_content_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer6.Add( self.m_result_list, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_result_content_panel.SetSizer( bSizer6 )
		self.m_result_content_panel.Layout()
		bSizer6.Fit( self.m_result_content_panel )
		self.m_grep_notebook.AddPage( self.m_result_content_panel, u"Content", False )
		
		fgSizer13.Add( self.m_grep_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_progressbar = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,2 ), wx.GA_HORIZONTAL )
		fgSizer13.Add( self.m_progressbar, 1, wx.ALIGN_CENTER|wx.ALL|wx.EXPAND, 5 )
		
		
		bFrameSizer.Add( fgSizer13, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bFrameSizer )
		self.Layout()
		self.m_statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.on_close )
		self.m_searchin_dir_picker.Bind( wx.EVT_DIRPICKER_CHANGED, self.on_dir_changed )
		self.m_search_regex_radio.Bind( wx.EVT_RADIOBUTTON, self.on_regex_enabled )
		self.m_search_text_radio.Bind( wx.EVT_RADIOBUTTON, self.on_text_enabled )
		self.m_filematchregex_radio.Bind( wx.EVT_RADIOBUTTON, self.on_filematch_regex_enabled )
		self.m_filematchtext_radio.Bind( wx.EVT_RADIOBUTTON, self.on_filematch_text_enabled )
		self.m_search_button.Bind( wx.EVT_BUTTON, self.on_search_click )
		self.m_result_file_list.Bind( wx.EVT_LEFT_DCLICK, self.on_file_dclick )
		self.m_result_list.Bind( wx.EVT_LEFT_DCLICK, self.on_content_dclick )
		self.m_result_list.Bind( wx.EVT_LIST_COL_CLICK, self.on_col_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_close( self, event ):
		event.Skip()
	
	def on_dir_changed( self, event ):
		event.Skip()
	
	def on_regex_enabled( self, event ):
		event.Skip()
	
	def on_text_enabled( self, event ):
		event.Skip()
	
	def on_filematch_regex_enabled( self, event ):
		event.Skip()
	
	def on_filematch_text_enabled( self, event ):
		event.Skip()
	
	def on_search_click( self, event ):
		event.Skip()
	
	def on_file_dclick( self, event ):
		event.Skip()
	
	def on_content_dclick( self, event ):
		event.Skip()
	
	def on_col_click( self, event ):
		event.Skip()
	
