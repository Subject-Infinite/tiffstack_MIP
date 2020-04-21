#To create Z stack of single time point from separate .tif files in specific folder

import os
from ij.io import DirectoryChooser
from ij import IJ, ImagePlus, VirtualStack
from ij.plugin import ZProjector

def maxZprojection(inputimg):
	zp = ZProjector(inputimg)
	zp.setMethod(ZProjector.MAX_METHOD)
	zp.doProjection()
	Zproj = zp.getProjection()
	return Zproj

sourceDir = DirectoryChooser("Choose directory to load stack from").getDirectory()
if not sourceDir:
	exit() #If you do not select a directory, terminates program
# Assumes all files have the same size
ImStack = None
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

imp = IJ.getImage()
print "waiting..."
outimp = maxZprojection(OnscreenImage)
outimp.show()
print "Max projection generated"

SaveQuery=input("Would you like to save the max proj? y = save, anything else = don't save")
savename = soureDir+"MIP.tif"
if SaveQuery.upper=='Y':
	RenameQuery=raw_input("Would you like to rename the max proj? (if not, will use directory name+MIP). y = yes, otherwise no")
	if RenameQuery.upper=='Y':
		savename = raw_input("type new name:")
	else:
		pass
	IJ.save(outimp, savename)
else:
	pass

exit()