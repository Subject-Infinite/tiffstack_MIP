# tiffstack_MIP
Opening a folder of tiffs into a single z stack and converting to MIP

ImageJ Macro

Opens a folder containing an image series of Z slices (single time point), and opens them into a single virtul stack.  
The macro then creates a maximum intensity projection (MIP) from the virtual stack and outputs that in a separate image.  
The program then offers the option to save the MIP, and rename the output MIP.

issues: Will not open multiple timepoints in 4D hyperstack, only works on single timepoint single channel data. (the code will technically run on multiple timepoints but the output will be garbled, it's a simple program)  

NOTE: I aim to add 4D hyperstack, multichannel support

NOTE: I aim to streamline GUI elements so source directory and prefix length selection are incorporated with main GUI window


The default save directory for the MIP is the folder from which the tiffs are being read. Setting a different save directory will have to be done via editting the saveDir variable at the start of the code. Set it to the path of the directory you want to save the MIP to, as the program will automatically output to the folder you read the tifs from, which may not be ideal for if you want to read that folder stack again in future.

----------


Made to be Fiji ImageJ (v1.52p) Jython compatible


----------


Running the macro:

1. ![macro_1](https://i.imgur.com/BmIBzWD.png)

From the plugins dropdown in Fiji ImageJ. Run from the Macros dropdown. Select the Zstack_MIP_creator_FIJI.py file

2. ![macro_2](https://i.imgur.com/aVlxxj9.png)

You will be prompted to select the directory in which your tiff sequence is held. As highlighted in the folder view window you can see there is a mix of prefixes in this folder. This plugin should sort between them and offer you the choice of which stacks to generate.

3. ![macro_3](https://i.imgur.com/XM8PgL5.png)

You will be prompted to input the length of prefix you want to create stacks of. Type in the length of common filetype to generate unique values from. e.g. If a folder contains files names IMAGEA_001, IMAGEA_002, IMAGEA_003, IMAGEB_001, IMAGEB_002, IMAGEB_003 the common prefix length is 6 (or 7). It will generate all unique values of the prefix length you specify.

4. ![macro_4](https://i.imgur.com/EjECC3q.png)

The program will generate 3D stacks and MIPs of your selections. 

The main GUI will open. On the left most panel, the unique prefixes of stacks are displayed. You can select one or more of these. For multiple selections, hold ctrl (or your OS's equivalent key) and click the stacks you are interested in generating. To select all, click the first value in the list, hold shift and click the last value in the list. The program will generate separate stacks and MIPs for all the selections you make. If the files are large, be wary of your RAM usage.

5. ![macro_5](https://i.imgur.com/cC3oDDk.png)

The program automatically specifies the file type as tif, but you can change this to any imageJ supported file extension. Select whether you want the the resultant MIPs to be saved or not. Regardless of save status, all selected items will still display.

6. ![macro 6](https://i.imgur.com/95ww8Sz.png)

Specify the directory into which you want the program to save the MIPs in. If you have selected multipl prefixes, it will save all resultant MIPs into this single directory. Their names will be their prefix + _MIP

7. ![macro_7](https://i.imgur.com/jh9VbMH.png)

Stacks and MIPs will open in separate windows. A non destructive text overlay is placed in the top left corner of every stack and MIP, displaying the prefix they derive from, so you know which one is which. 
