#To create Z stack of single time point from separate .tif files in specific folder

import os
from ij.io import DirectoryChooser
from ij import IJ, ImagePlus, VirtualStack
from ij.plugin import ZProjector
from javax.swing import JOptionPane

def maxZprojection(inputimg):
	zp = ZProjector(inputimg)
	zp.setMethod(ZProjector.MAX_METHOD)
	zp.doProjection()
	Zproj = zp.getProjection()
	return Zproj

sourceDir = DirectoryChooser("Choose directory to load stack from").getDirectory()
os.chdir(sourceDir)
curdir = os.path.split(os.getcwd())[1] 
saveDir = sourceDir # for custom saving directory, simply replace this particular 'sourceDir' with the save directory of choice. 
# Insert new save directory up until the final '\' here, e.g. saveDir = "C:\Users\UserName\Documents\" or the equivalent for your operating system
#default save directory will just save the output MIP into the same folder the other tifs of the z stack came from. may not be optimal.

if not sourceDir:
	exit() # If you do not select a directory, terminates program
# Assumes all files have the same size
ImStack = None
#print "os.walk: ", list(os.walk(sourceDir))
for root, directories, filenames in os.walk(sourceDir):
	for filename in filenames:
	  # Skip non-TIFF files
	  if not filename.endswith(".tif"):
		continue
	  path = os.path.join(root, filename)
	  # Upon finding the first image, initialize the VirtualStack
	  if ImStack is None:
		imp = IJ.openImage(path)
		ImStack = VirtualStack(imp.width, imp.height, None, sourceDir)
	  # Add a slice, relative to the sourceDIr
	  ImStack.addSlice(path[len(sourceDir):])

OnscreenImage = ImagePlus(sourceDir,ImStack)
OnscreenImage.show()

print "Generating MIP, waiting..."
outimp = maxZprojection(OnscreenImage) #generate max projection
outimp.show()
print "Max projection generated"

###To remove save functionality, just remove all beyond here-

SaveQuery = JOptionPane.showInputDialog(None, "Would you like to save the max proj? y = save, anything else = don't save")

if SaveQuery.upper()=='Y':
	RenameQuery = JOptionPane.showInputDialog(None, "Would you like to rename the max proj? (if not, will use directory name+_MIP). y = yes, otherwise no")
	if RenameQuery.upper()=='Y':
		curdir = JOptionPane.showInputDialog(None, "Input new name for Max projection")
	savename = saveDir+curdir+"_MIP.tif"
	print "saving...."
	IJ.save(outimp, savename)
	print "saved as", savename
else:
	print "MIP not saved"
