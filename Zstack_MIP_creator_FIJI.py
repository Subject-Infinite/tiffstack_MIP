import os
from ij.io import DirectoryChooser
from javax.swing import JFrame, JPanel, JLabel, JList, JButton, ListSelectionModel, JOptionPane, JScrollPane, JTextArea, JSplitPane, JRadioButton, Box, ButtonGroup, BoxLayout
from java.awt import BorderLayout, Dimension

def obtain_prefixes():
	sourceDir = DirectoryChooser("Choose directory to load stack from").getDirectory()
	os.chdir(sourceDir)
	
	curdir=os.getcwd()
	listdire=os.listdir(curdir)
	
	prefixlist = []
	prefix_len = JOptionPane.showInputDialog(None, "how long is the file prefix to group by?(integer value only)")
	for name in listdire:
		if ".tif" in name:
			prefixname = name[:int(prefix_len)]
			prefixlist.append(prefixname)
	
	unique_prefix = sorted(set(prefixlist))
	pref_dict = {}
	#print unique_prefix
	
	for a in unique_prefix:
		pref_list = []
		for b in listdire:
			if b.startswith(a):
				pref_list.append(b)
		pref_dict[a]=pref_list
	return pref_dict

class choice_gui:
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
		else:
			print "cancelled"
		return self.itemSelected
		
	def __init__(self, lst):
		self.frame = JFrame("Image Selection")
		self.frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
		self.frame.setLocation(100,100)
		self.frame.setSize(640,250)

		self.frame.setLayout(BorderLayout())
		self.lang=lst

		self.lst = JList(self.lang, valueChanged = self.listSelect)

		self.frame.add(self.lst, BorderLayout.NORTH)
		self.lst.selectionMode = ListSelectionModel.MULTIPLE_INTERVAL_SELECTION
		self.button1 = JButton('Select item(s)', actionPerformed = self.clickhere)
#Save option radio button	
		self.radiobutton1 = JRadioButton("Open selected 3D stacks and max projections \n and save max projections", True)
		self.radiobutton2 = JRadioButton("Open selected 3D stacks and max projections \n and DO NOT save max projections")		
		buttonpanel = JPanel()
		grp = ButtonGroup()
		grp.add(self.radiobutton1)
		grp.add(self.radiobutton2)
		buttonpanel.setLayout(BoxLayout(buttonpanel, BoxLayout.Y_AXIS))
		buttonpanel.add(Box.createVerticalGlue())
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

	def __str__(self):
		return self.outputlist



dict1 = obtain_prefixes()
obtain_prefixes_keys = list(dict1.keys())
print "keys = ", obtain_prefixes_keys
choice = choice_gui(obtain_prefixes_keys)
print "choice.stuff: ", choice.clickEx()
#print os.getcwd()