Python-Remote-Sensing
=====================

Contact information
-------------------
For any suggestion, complaint or just for help, don't hesitate on contacting us

 Denis Araujo Mariano
 denis.mariano@usp.br
 
 William Foschiera
 wfoschiera@gmail.com

You can contact us in English, Portuguese of even in Spanish.

First things first
---------------------------
Up till now, the scripts we created in python need some packages installed for working fine. If you use Linux systems, all this can be done easily, for example in Ubuntu:
Go to the terminal and then:

sudo apt-get install python
sudo apt-get install python-numpy
sudo apt-get install python-gdal

However, if you're using Windows, one easy way for getting over these is by installling QGIS. 
The QGIS will install all those packages on your system.

NDVI and EVI calculation
------------------------

The NDVI and EVI script easily calculates these Vegetation Indices.
You just have to set up a folder with you RED images in Geotiff, the same for NIR and also for BLUE (in the case of EVI).

If you're using Landsat images downloaded from USGS system, it's not necessary to be worried about conversion from Digital Number to Surface Reflectance.
By using MODIS, you don't have to care about this as well, however, all the input images have to be corrected by a factor (divide by 10000), this is not necessary if you're calculating only the NDVI, but for EVI this is needed.


TCI (Temperature Condition Index) (Kogan, 1995) calculation script
------------------------------------------------------------------
For calculating this index you have to generate some previous data outside, for example in QGIS. Pretty easy as well, I will explain how to do that just like for a baby.

This text is also available into the script file.

INPUT FILES:
    This script was created for working with MODIS LST data.
    You just need a raster in geotiff for the maximum of the series, another
    for the minimum and of course, the whole image series for doing the
    series of TCI images.

CREATING MAX and MIN images:

    You have to setup up the image for Max and Min temperature over a time series.
    This can be easily created using QGIS > Grass Tools > r.series.:
    1 - In QGIS, enable the sextante toolbox
    2 - This is gonna hurt... load all the input images, I mean, the whole time
        series. 
    3 - find the GRASS commands and go to r.series
    4 - Open one image from the summer, any hot day and check its histogram
    5 - Take the minimum and max, it should be about 14000 to 16000.
    6 - In the r.series tool click 'Show advanced parameters' and them put
        the values found in item 5.
    7 - Set 'Propagate NULLs' to 'No'
    8 - Choose 'Aggregate operation' to 'maximum' and set the output file.
    9 - Repeat for the operation for 'mininum'.
    
Contact information
-------------------
For any suggestion, complaint or just for help, don't hesitate on contacting us

 Denis Araujo Mariano
 denis.mariano@usp.br
 
 William Foschiera
 wfoschiera@gmail.com
