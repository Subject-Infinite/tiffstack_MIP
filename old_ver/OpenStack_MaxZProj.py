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
	exit() # If you do not select a directory, terminates program
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

print "Generating MIP, waiting..."
outimp = maxZprojection(OnscreenImage)
outimp.show()
print "Max projection generated"

#@ String (label="Would you like to save the max proj? y = save, anything else = don't save", description="Save as") SaveQuery
	#@output String greeting
print SaveQuery
savename = sourceDir+"_MIP.tif"
if SaveQuery.upper=='Y':

	#@ String (label="Would you like to rename the max proj? (if not, will use directory name+MIP). y = yes, otherwise no", description="Save as rename") RenameQuery
	#@output String greeting
	print "Hello"
	
	# RenameQuery=raw_input("Would you like to rename the max proj? (if not, will use directory name+MIP). y = yes, otherwise no")
	if RenameQuery.upper=='Y':
		#@ String (label="type new name", description="Rename") savename
		#@output String greeting
		
		# savename = raw_input("type new name:")
		print "hello"
	else:
		pass
	IJ.save(outimp, savename)
else:
	pass

#exit()