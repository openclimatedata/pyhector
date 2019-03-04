# Windows Installation Guide

This guide explains one way of installing pyhector on a windows machine. This involves cloaning the pyhector repository and making changes to the setup.py file before installing it manually.

## Installing and building boost libraries

Download the boost library as a zipfile (or other available formats) from https://www.boost.org/users/history/. I downloaded version "boost\_1\_66\_0.zip" because right now Hector is only tested through this version. Wherever you choose to extract the files on your computer, the folder called "boost\_1\_66\_0" will be referred to as your boost subdirectory for the rest of the instructions.

I had to compile the boost libraries by doing the following:
- Run the Windows Batch File named "bootstrap" (this should be in the boost subdirectory). This will create additional files in the boost subdirectory. 
- Run the "b2.exe". This will compile the libraries and puts them in the "bin.v2" folder in the boost subdirectory. This step will take several minutes.

Then to make the compiled libraries available to python, I had to copy the following 2 files into my "anaconda3/libs" folder (this will be different if you aren't using anaconda. There are  other places that python also looks for compiled libraries, but I could not figure out how to add to that list of paths, and instead decided to just copy the necessary files into this folder)
- "bin.v2\libs\filesystem\build\msvc-14.1\release\link-static\threadapi-win32\threading-multi\libboost\_filesystem-vc141-mt-x32-1\_66.lib"
- "bin.v2\libs\system\build\msvc-14.1\release\link-static\threadapi-win32\threading-multi\libboost\_system-vc141-mt-x32-1\_66.lib"

After copying them into the "anaconda3/libs" folder, rename them to "boost\_filesystem.lib" and "boost\_system.lib" (the names that pyhector is looking for during build time.)

## Installing pyhector

Download the pyhector repository using git:
`git clone https://github.com/openclimatedata/pyhector.git --recursive`

Then do the following:
- modify the list of `include_dirs` on line 59 to include the path to your boost subdirectory. This will give the libpyhector Extension defined here access to all of the libraries that are only header files (for example, the numeric library). The two necessary _compiled_ libraries (system and filesystem) we already took care of in the above instructions. 
- Run `python setup.py build`. This creates the directory "pyhector/build". 
- In the build directory, there should be a file "lib.win-amd64-3.7\pyhector/_binding.cp37-win\_amd64.pyd", or something similarly named.
- Copy this pyd file into the "pyhector/phyector" folder and rename it to "_binding.pyd".
- Then run `python setup.py install`