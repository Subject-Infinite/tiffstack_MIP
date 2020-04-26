import os
from ij.io import DirectoryChooser
from ij import IJ, ImagePlus, VirtualStack, WindowManager
from ij.plugin import ZProjector
from javax.swing import JFrame, JPanel, JLabel, JList, JButton, ListSelectionModel, JOptionPane, JScrollPane, JTextArea, JSplitPane, JRadioButton, Box, ButtonGroup, BoxLayout
from java.awt import BorderLayout, Dimension
import threading

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
		#print unique_prefix
		
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
		self.exeunt = JOptionPane.showConfirmDialog(None, "You have chosen to make MIPs out of \n" + str(self.itemSelected) + "\n Proceed?" , "Proceed?", JOptionPane.YES_NO_OPTION)
		self.clickEx()
		
	def clickEx(self):
		if self.exeunt == JOptionPane.YES_OPTION:
			print "confirmed"
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
		#ImStack = None
		#print "os.walk: ", list(os.walk(sourceDir))
		for a in self.itemSelected:#######
			ImStack = None
			#print "createMIP a = ", a
			for filename in self.dict1.get(a):
				#print "createMIP self dict1:::", self.dict1.get(a)
				self.savfileName = filename[:-4]
				#print "createMIP filename--", filename
	 			# Skip non-TIFF files
				if not filename.endswith(".tif"):
					continue
				#path = os.path.join(root, filename)########
	 			path = self.sourceDir + filename
	 			#print "path = ", path
				# Upon finding the first image, initialize the VirtualStack
				if ImStack is None:
					#print "path...", path
					imp = IJ.openImage(path)
					#WindowManager.makeUniqueName(a)
					ImStack = VirtualStack(imp.width, imp.height, None, self.sourceDir)
				# Add a slice, relative to the sourceDIr
				#print "adding ", filename
				ImStack.addSlice(filename)
			
			OnscreenImage = ImagePlus(self.sourceDir,ImStack)
			OnscreenImage.show()
			
			print "Generating MIP, waiting..."
			self.outimp = self.maxZprojection(OnscreenImage) #generate max projection
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
		
		self.frame = JFrame("Image Selection")
		self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
		self.frame.setLocation(100,100)
		self.frame.setSize(640,250)

		self.frame.setLayout(BorderLayout())
####run everything from within the class? Insert def obtain_prefixes() and call obtain_prefixes() here? Bundle everything into class, MIP creation further down after box params
		
		self.dict1 = self.obtain_prefixes()
		lst = list(self.dict1.keys())
		
		self.lang=lst

		self.lst = JList(self.lang, valueChanged = self.listSelect)

		self.frame.add(self.lst, BorderLayout.NORTH)
		self.lst.selectionMode = ListSelectionModel.MULTIPLE_INTERVAL_SELECTION
		self.button1 = JButton('Select item(s)', actionPerformed = self.clickhere)
#Save option radio button	
		self.radiobutton1 = JRadioButton("Open selected 3D stacks and max projections \n and save max projections", True)
		self.radiobutton2 = JRadioButton("Open selected 3D stacks and max projections \n and DO NOT save max projections")		
		buttonpanel = JPanel()
		infoLabel = JLabel("Hold ctrl and click multiple prefixes to select multiple options \n will load stacks and MIPs separately")
		grp = ButtonGroup()
		grp.add(self.radiobutton1)
		grp.add(self.radiobutton2)
		buttonpanel.setLayout(BoxLayout(buttonpanel, BoxLayout.Y_AXIS))
		buttonpanel.add(Box.createVerticalGlue())
		buttonpanel.add(infoLabel)
		buttonpanel.add(self.radiobutton1)
		buttonpanel.add(self.radiobutton2)
		buttonpanel.add(Box.createRigidArea(Dimension(0,25)))
#split list and radiobutton pane (construct overall window)		
		spl = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, JScrollPane(self.lst),JLabel("rightpane"))
		spl.leftComponent = JScrollPane(self.lst)
		spl.rightComponent = buttonpanel

		self.frame.add(spl)
		self.frame.add(self.button1, BorderLayout.SOUTH)

		self.frame.setVisible(True)



choice = choice_gui()
choice
	