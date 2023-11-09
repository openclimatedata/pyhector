# Windows Installation Guide

This guide explains one way of installing pyhector on a windows machine. This involves cloaning the pyhector repository and making changes to the setup.py file before installing it manually. This feels like an inelegant (and potentially problematic) work-around to get pyhector running, but I hope it can help others or invite feedback on how to improve this process.

The first section about setting up boost may not apply if you have already installed and/or built the necessary libraries through Visual Studio. These specific steps were necessary on my machine for python to be able to find the compiled libraries.  

## Installing and building boost libraries

Download the boost library as a zipfile (or other available formats) from https://www.boost.org/users/history/. I downloaded version "boost\_1\_66\_0.zip" because right now Hector is only tested through this version. Wherever you choose to extract the files on your computer, the folder called "boost\_1\_66\_0" will be referred to as your boost subdirectory for the rest of the instructions.

I had to compile the boost libraries by doing the following:
- Run the Windows Batch File named "bootstrap" (this should be in the boost subdirectory). This will create additional files in the boost subdirectory. 
- Run the "b2.exe" file. This will compile the libraries and put them in a folder called "bin.v2" in the boost subdirectory. This step will take several minutes.

Then to make the compiled libraries available to python, I had to copy the following 2 files into my "anaconda3/libs" folder (this will be different if you aren't using anaconda. There are  other places that python also looks for compiled libraries, but I could not figure out how to add to that list of paths):
- "bin.v2\libs\filesystem\build\msvc-14.1\release\link-static\threadapi-win32\threading-multi\libboost\_filesystem-vc141-mt-x32-1\_66.lib"
- "bin.v2\libs\system\build\msvc-14.1\release\link-static\threadapi-win32\threading-multi\libboost\_system-vc141-mt-x32-1\_66.lib"

After copying these 2 files into the "anaconda3/libs" folder, rename them to "boost\_filesystem.lib" and "boost\_system.lib" (the names that pyhector is looking for during build time).

## Installing pyhector

Download the pyhector repository using git:

`git clone https://github.com/openclimatedata/pyhector.git --recursive`

Then do the following:
- Open the "pyhector/setup.py" file in an editor
- Modify the list of `include_dirs` on line 59 to include the path to your boost subdirectory. This will give the libpyhector Extension defined here access to all of the libraries that are only header files, for example, the numeric library. 
- I also needed to delete "m" from the list of libraries on line 65. This is inexplicable to me, but so far this hasn't caused problems in running pyhector. Either somehow my c++ setup already has access to a math library, or nothing I've tried to do yet with pyhector necessitated this functionality. (The reason I didn't also copy an m.lib file into the "anaconda3/libs" folder like I did for boot\_system.lib and boost\_filesystem.lib was that in the folder for the compiled math boost library, there were several different library files and I wasn't sure which one to choose.) 
- Run `python setup.py build`. This creates the directory "pyhector/build". 
- In the build directory, there should now be a file "lib.win-amd64-3.7/pyhector/\_binding.cp37-win\_amd64.pyd", or something similarly named.
- Copy this pyd file into the "pyhector/phyector" folder and rename it to "\_binding.pyd" (the module name pyhector will look for).
- Then run `python setup.py install`