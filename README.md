# tiffstack_MIP
Opening a folder of tiffs into a single z stack and converting to MIP

ImageJ Macro

Opens a folder containing an image series of Z slices (single time point), and opens them into a single virtul stack.  
The macro then creates a maximum intensity projection (MIP) from the virtual stack and outputs that in a separate image.  
The program then offers the option to save the MIP, and rename the output MIP.

issues: Will not open multiple timepoints in 4D hyperstack, only works on single timepoint data. (the code will technically run on multiple timepoints but the output will be garbled, it's a simple program)  


The default save directory for the MIP is the folder from which the tiffs are being read. Setting a different save directory will have to be done via editting the saveDir variable at the start of the code. Set it to the path of the directory you want to save the MIP to, as the program will automatically output to the folder you read the tifs from, which may not be ideal for if you want to read that folder stack again in future.

----------


Made to be Fiji ImageJ (v1.52p) Jython compatible


----------


Running the macro:

1. ![macro_1](https://i.imgur.com/BmIBzWD.png)

From the plugins dropdown in Fiji ImageJ. Run from the Macros dropdown. Select the OpenStack_MaxZProj_2_fiji.py file

2. ![macro_2](https://i.imgur.com/57TTVtf.png)

You will be prompted to select the directory in which your tiff sequence is held

3. ![macro_3](https://i.imgur.com/fMaAZUG.png)

This will generate a virtual stack oif your z slices, and the MIP, and it will ask if you want to save. type y for further save options, type anything else if you don't want to save the MIP

4. ![macro_4](https://i.imgur.com/G0jnTmK.png)

Prompt to rename MIP output

5. ![macro_5](https://i.imgur.com/gFpiYJg.png)

prompt for what you wish to rename to

6. ![macro_6](https://i.imgur.com/FXXmCck.png)

The MIP and virtual stack are kept separate, if you wish to make separate manipulations.

