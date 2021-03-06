###A Fiji ImageJ plugin to pull stacks of varying prefixes from a folder. Only works on single channel, single timepoint images for now

import os
from ij.io import DirectoryChooser
from ij import IJ, ImagePlus, VirtualStack, WindowManager
from ij.plugin import ZProjector
from ij.gui import Roi, Overlay, TextRoi
from javax.swing import JFrame, JPanel, JLabel, JList, JButton, ListSelectionModel, JOptionPane, JScrollPane, JTextArea, JSplitPane, JRadioButton, Box, ButtonGroup, BoxLayout, JTextField, SwingConstants
from java.awt import BorderLayout, Dimension, Font, Color, Component, FlowLayout
class choice_gui:

################ input function

	def obtain_prefixes(self):
		self.sourceDir = DirectoryChooser("Choose directory to load stack from").getDirectory()
		os.chdir(self.sourceDir)
		
		curdir=os.getcwd()
		listdire=os.listdir(curdir)
		
		prefixlist = []
		prefix_len = JOptionPane.showInputDialog(None, "how long is the file prefix to group by?(integer value only)")
		for name in listdire:
			if ".tif" in name:
				prefixname = name[:int(prefix_len)]
				prefixlist.append(prefixname)
		
		unique_prefix = sorted(set(prefixlist))
		self.pref_dict = {}
		
		for a in unique_prefix:
			pref_list = []
			for b in listdire:
				if b.startswith(a):
					pref_list.append(b)
			self.pref_dict[a]=pref_list
		return self.pref_dict

################### event handling

	def listSelect(self, event):
		self.index = self.lst.selectedIndex
			
	def clickhere(self,event):
		self.lst.selectionMode = (ListSelectionModel.MULTIPLE_INTERVAL_SELECTION)
		print "clicked"
		self.itemSelected = list(sorted(self.lst.selectedValues[:]))
		print "item selected:", self.itemSelected
		if self.radiobutton1.isSelected():
			self.saveState = "Y"
			print "Save MIPs!"
		if self.radiobutton2.isSelected():
			self.saveState = "N"
			print "Don't save MIPs!"
		self.exeunt = JOptionPane.showConfirmDialog(None, "You have chosen to make MIPs out of \n {} \n proceed?".format(str(self.itemSelected)), "Proceed?", JOptionPane.YES_NO_OPTION)
		self.clickEx()
		
	def clickEx(self):
		if self.exeunt == JOptionPane.YES_OPTION:
			print "confirmed"
			self.fileExt = str(self.filetype.getText())
			self.frame.setVisible(False)
			if self.saveState=="Y":
				self.saveDir = DirectoryChooser("Choose directory to save MIPs to").getDirectory()
			self.createMIP()
		else:
			print "cancelled"

################### ImageJ

	def maxZprojection(self, inputimg):
		zp = ZProjector(inputimg)
		zp.setMethod(ZProjector.MAX_METHOD)
		zp.doProjection()
		Zproj = zp.getProjection()
		return Zproj

	def createMIP(self):
		print "starting createMIP"
		for a in self.itemSelected:
			ImStack = None
			for filename in self.dict1.get(a):
				self.savfileName = a
				if not filename.endswith(self.fileExt):
					continue
	 			path = self.sourceDir + filename
				# Upon finding the first image, initialize the VirtualStack
				if ImStack is None:
					imp = IJ.openImage(path)
					ImStack = VirtualStack(imp.width, imp.height, None, self.sourceDir)
				# Add a slice, relative to the sourceDIr
				ImStack.addSlice(filename)
			#adding text overlay to output images so we can differentiate them. Overlay is non destructive - does not affect pixel values of image, and can be selected and deleted
			prefix_overlay = Overlay()
			font=Font("SansSerif", Font.PLAIN,10)
			roi = TextRoi(0,0,a)
			roi.setStrokeColor(Color(1.00,1.00,1.00))
			prefix_overlay.add(roi)
			#
			OnscreenImage = ImagePlus(self.sourceDir,ImStack)
			OnscreenImage.setOverlay(prefix_overlay)
			OnscreenImage.show()
			
			print "Generating MIP, waiting..."
			self.outimp = self.maxZprojection(OnscreenImage) #generate max projection
			self.outimp.setOverlay(prefix_overlay)
			self.outimp.show()
			print "Max projection generated"
			if self.saveState=="Y":
				self.saveMIP()
			print "Finished!"

	def saveMIP(self):
		curdir = os.path.split(os.getcwd())[1] 
		savename = self.saveDir+curdir+self.savfileName+"_MIP.tif"
		print "savename = ", savename
		print "saving...."
		IJ.save(self.outimp, savename)
		print "saved as", savename


###################
				
	def __init__(self):
#obtain prefixes from folder		
		self.dict1 = self.obtain_prefixes() #Run prefix selection function - sets source directory, requests prefix size, outputs prefix dictionary
		lst = list(self.dict1.keys()) #pull prefixes only, as list		
		self.lang=lst
		self.lst = JList(self.lang, valueChanged = self.listSelect) # pass prefix list to GUI selection list
		
# general GUI layout parameters, no data processing here
		self.frame = JFrame("Image Selection")
		self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
		self.frame.setLocation(100,100)
		self.frame.setSize(800,350)
		self.frame.setLayout(BorderLayout())

		self.frame.add(self.lst, BorderLayout.NORTH)
		self.lst.selectionMode = ListSelectionModel.MULTIPLE_INTERVAL_SELECTION
		self.button1 = JButton('Select item(s)', actionPerformed = self.clickhere)
		
#Save option radio buttons and file extension selection	
		#set main right panel (sub panels will fit within this)
		rightpanel = JPanel()
		rightpanel.setLayout(BoxLayout(rightpanel, BoxLayout.Y_AXIS))
		
		#set up savestate panel		
		buttonpanel = JPanel()
		self.radiobutton1 = JRadioButton("Open selected 3D stacks and max projections \n and save max projections", True)
		self.radiobutton2 = JRadioButton("Open selected 3D stacks and max projections \n and DO NOT save max projections")		
		infoLabel = JLabel("<html>Hold ctrl and click multiple prefixes to select multiple options. Will load stacks and MIPs separately <br><br> Type file extension in text field below:</html>", SwingConstants.LEFT)
		grp = ButtonGroup()
		grp.add(self.radiobutton1)
		grp.add(self.radiobutton2)
		#buttonpanel.setLayout(BoxLayout(buttonpanel, BoxLayout.Y_AXIS))
		buttonpanel.add(Box.createVerticalGlue())
		buttonpanel.add(infoLabel)
		buttonpanel.add(Box.createRigidArea(Dimension(0,5)))
		buttonpanel.add(self.radiobutton1)
		buttonpanel.add(Box.createRigidArea(Dimension(0,5)))
		buttonpanel.add(self.radiobutton2)
		
		#file extension instruction panel
		infopanel = JPanel()
		infopanel.setLayout(FlowLayout(FlowLayout.LEFT))
		infopanel.setMaximumSize(infopanel.setPreferredSize(Dimension(650,100)))
		infopanel.add(infoLabel)

		#file extension input
		inputPanel = JPanel()
		inputPanel.setLayout(BoxLayout(inputPanel, BoxLayout.X_AXIS))
		self.filetype = JTextField(".tif",15)
		self.filetype.setMaximumSize(self.filetype.getPreferredSize())	
		inputPanel.add(self.filetype)
			
		########### WIP - integrate prefix selection with main pane, with dynamically updating prefix list
		##infoLabel3 = JLabel("how long is the file prefix to group by?(integer value only)")
		##self.prefix_init = JTextField()
		##buttonpanel.add(infoLabel3)
		##buttonpanel.add(self.prefix_init)
		########### !WIP
		#add file extension and savestate panels to main panel
		rightpanel.add(infopanel)
		rightpanel.add(inputPanel)
		rightpanel.add(buttonpanel,BorderLayout.EAST)
		
#split list and radiobutton pane (construct overall window)
		spl = JSplitPane(JSplitPane.HORIZONTAL_SPLIT)
		spl.leftComponent = JScrollPane(self.lst)
		spl.setDividerLocation(150)
		spl.rightComponent = rightpanel
		self.frame.add(spl)
		self.frame.add(self.button1, BorderLayout.SOUTH)
		
# GUI layout done, initialise GUI to select prefixes, file extension and save option
		self.frame.setVisible(True)

choice = choice_gui()
choice
