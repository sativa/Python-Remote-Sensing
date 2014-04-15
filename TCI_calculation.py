# -*- coding: utf-8 -*-
"""
SCRIPT FOR CALCULATING THE TEMPERATURE CONDITION INDEX (TCI)(Kogan, 1995)

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

SOME LINES to EDIT    
    Ok, now you have the maximum and mininum of your time series, you will 
    then edit some lines in this script as indicated in it.
    
For any question or suggestion, write to the authors.

@author: William Foschiera and Denis Araujo Mariano
email: wfoschiera@gmail.com and denis.mariano@usp.br
Remote Sensing Students at National Institue for Space Resarch
INPE - Brazil

"""

import gdal, os, glob, time
import numpy as np

startTime = time.time()

os.chdir('/media/denis/DATA/Drought_tests3')

driver = gdal.GetDriverByName('GTiff')

#EDIT THESE LINES
#Put here the whole path to the images you just created using QGIS as suggested
maxpath = '/media/denis/DATA/Drought_tests3/MINMAX/2002265-2003089day_max.tif'
minpath = '/media/denis/DATA/Drought_tests3/MINMAX/2002265-2003089day_min.tif'

# this is your output directory. If you haven'created it yet, just type
# the here and the script will create it for you. Don't worry about it.
outputPath = '/media/denis/DATA/Drought_tests3/TCI/'
#STOP EDITTING
#you have to edit the final lines of this script
# that one like this     TCI('/media/denis/DATA/Drought_tests3/',j)  


#Don't mess after this point#
if not os.path.exists(outputPath): os.makedirs(outputPath)

t_max = gdal.Open(maxpath)
tmin = gdal.Open(minpath).ReadAsArray()

tmax = gdal.Open(maxpath).ReadAsArray()
geo = t_max.GetGeoTransform()  # get the datum
proj = t_max.GetProjection()   # get the projection 
row = t_max.RasterYSize #get the number of rows
col = t_max.RasterXSize #get the number of columns
shape = (row,col)


#There is a little trick here. For avoiding division by zero and considering
#the MODIS LST product values range from about 14000 to 16000,
#there isn't any problem on summing 1 or 2 to they
x = np.ones(shape, dtype=float) #create a matrix of ones
tmin = tmin + x 
tmax = tmax + 2*x

#TEMPERATURE CONDITION INDEX
def TCI(path,filename):
    '''
    path: the path to the input images (not the max nor min)
    filename: the filenames for getting the input and creating the output
    '''
    #import gdal, os, glob
    #import numpy as np
    #You can import these packages again just in case of you wanting to use
    #the TCI function from outside of this script
    b = filename.split('/')[-1]
    tactual = gdal.Open(path + b).ReadAsArray() + x   
    #print i.split('/media/denis/DATA/Drought_tests3/')
    tci_ = (tmax - tactual)/(tmax - tmin)
    tci_saida = driver.Create(path + '/TCI/TCI_'+b, shape[1], shape[0], 1, gdal.GDT_Float32)
    tci_saida.SetGeoTransform(geo) # set the datum
    tci_saida.SetProjection(proj)  # set the projection
    tci_saida.GetRasterBand(1).WriteArray(tci_)           
    return tci_saida
    
#EDIT THESE LINES, be careful in the for loop you have to keep the *.tif    
for j in glob.glob('/media/denis/DATA/Drought_tests3/*.tif'):
    TCI('/media/denis/DATA/Drought_tests3/',j)  
#STOP EDITTING

    
print 'The operation took ', time.time() - startTime, 'seconds.'
