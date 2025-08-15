# UGA_Optogenetics

Program developed in Ptyhon to control the Hamamtsu Orca-Flash 4.0 V3 camera and the Texas Instruments DLP lightcrafter 4500 in an optogenetics experiment. 
The system reaquires the scipy library, pyQT 5 and the usb.core library and drivers for the DLP. Anaconda was used to handle the packages.  
The main class is TIRF_GUI and it runs the user interface required to launch the experiment.
The outcome files are saved in the folder where the main class is located under the name 'sequence.tiff' with increasing filname indexing. 
The files in this repository are the ealiest version.
Some known bugs:
-  There is a start-up routine of the DLP that illuminates the sample before the experiment is running so a shutter is needed.
- The calibration button must be pressed twice until the user can observe the calibrating pattern. (the pattern is already projected on the sample but Python is snaping the image before the projection for an unknown reason, so far)
- The calibration routine must be checked as there still exists a shift in the adjusted vertices.
- the red LED current field is not being used as the LED was deactivated to obtain perfect black.

For some extra information please create an issue. 
f
