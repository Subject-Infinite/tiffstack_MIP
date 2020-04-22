# tiffstack_MIP
Opening a folder of tiffs into a single z stack and converting to MIP

ImageJ Macro

Opens a folder containing an image series of Z slices (single time point), and opens them into a single virtul stack.  
The macro then creates a maximum intensity projection (MIP) from the virtual stack and outputs that in a separarte image.  
The program then offers the option to save the MIP, and rename the output MIP.  

issues: Will not open multiple timepoints in 4D hyperstack, only works on single timepoint data. (the code will technically run on multiple timepoints but the output will be garbled, it's a simple program)  
Setting save directory will have to be done via editting the saveDir variable at the start of the code. Set it to the path of the directory you want to save the MIP to, as the program will automatically output to the folder you read the tifs from, which may not be ideal for if you want to read that folder stack again in future.  


Made to be Fiji ImageJ (v1.52p) Jython compatible
