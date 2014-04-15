# -*- coding: utf-8 -*-
"""
CALCULATING EVI and NDVI from GeoTiff images

Created on Mon Apr 14 15:38:18 2014

@author: William Foschiera & Denis Araujo Mariano
contact: wfoschiera@gmail.com , denis.mariano@usp.br
------------------------------------------------------
For using this script, you have to setup the folders for the RED, NIR and BLUE
images in .tif. 

"""

import gdal, os, glob, time
import numpy as np
startTime = time.time()
#os.chdir('/media/denis/DATA/Drought_tests3')


#This path you have to edit
#It is not necessary to creater the Output folders
#You just have to set'em up with the same root of your
#RED, NIR and BLUE folders
caminhoRED = '/media/denis/DATA/Drought_tests3/RED/*.tif'
caminhoNIR = '/media/denis/DATA/Drought_tests3/NIR/*.tif'
caminhoBLUE = '/media/denis/DATA/Drought_tests3/BLUE/*.tif'
#caminhoNIR2 = '/media/denis/DATA/Drought_tests3/NIR2/*.tif'

outputPath = '/media/denis/DATA/Drought_tests3/EVI/'
if not os.path.exists(outputPath): os.makedirs(outputPath)
    
outputPath = '/media/denis/DATA/Drought_tests3/NDVI/'
if not os.path.exists(outputPath): os.makedirs(outputPath)  
    
#outputPath = '/media/denis/DATA/Drought_tests3/NDWI/'
#if not os.path.exists(outputPath): os.makedirs(outputPath)    
    
#Please, don't mess after this point except for the NDVI and EVI
#lines at the end of this script

blue = []
for j in glob.glob(caminhoBLUE):
    b = j.split('/')
    c = b[-1]
    blue.append(c)


red = []
for j in glob.glob(caminhoRED):
    b = j.split('/')
    c = b[-1]
    red.append(c)
#print red

#Cria a lista das imagens NIR
nir = []
for j in glob.glob(caminhoNIR):
    b = j.split('/')
    c = b[-1]
    nir.append(c)

#Cria a lista das imagens NIR2
'''
nir2 = []
for j in glob.glob(caminhoNIR2):
    b = j.split('/')
    c = b[-1]
    nir2.append(c)
'''    
#Cria a lista com os nomes das imagens de saida
out = []
for i in range(len(nir)):
    b = nir[i].split('_b')
    b = b[-2] + '.tif'
    out.append(b)
    
#print out 
        
def NDVI(path,red,nir,out):
    '''
    path: caminho onde estao os arquivo
    nir: lista de imagens da banda 1.
    red: lista de imagens da banda 2.
    '''
    assert len(nir) == len(red)
    datum = gdal.Open(path + '/RED/' + red[0])
    row = datum.RasterYSize
    col = datum.RasterXSize
    shape = (row,col)
    driver = gdal.GetDriverByName('GTiff')
    geo = datum.GetGeoTransform()  # get the datum
    proj = datum.GetProjection()   # get the projection       
    for i in range(len(nir)):
        REDactual = gdal.Open(path + '/RED/' + red[i]).ReadAsArray()
        NIRactual = gdal.Open(path + '/NIR/' + nir[i]).ReadAsArray()
        NDVI = (NIRactual-REDactual)/(NIRactual+REDactual)
        ndvi_saida = driver.Create(path + '/NDVI/'+ 'NDVI_' + out[i], shape[1], shape[0], 1, gdal.GDT_Float32)
        ndvi_saida.SetGeoTransform(geo) # set the datum
        ndvi_saida.SetProjection(proj)  # set the projection
        ndvi_saida.GetRasterBand(1).WriteArray(NDVI) 
    return ndvi_saida
    
def EVI(path,red,nir,blue,out):
    '''
    path: caminho onde estao os arquivo
    nir: lista de imagens da banda 1.
    red: lista de imagens da banda 2.
    '''
    assert len(nir) == len(red) and len(red) == len(blue)
    datum = gdal.Open(path + '/RED/' + red[0])
    row = datum.RasterYSize
    col = datum.RasterXSize
    shape = (row,col)
    driver = gdal.GetDriverByName('GTiff')
    geo = datum.GetGeoTransform()  # get the datum
    proj = datum.GetProjection()   # get the projection       
    for i in range(len(nir)):
        REDactual = gdal.Open(path + '/RED/' + red[i]).ReadAsArray()
        NIRactual = gdal.Open(path + '/NIR/' + nir[i]).ReadAsArray()
        BLUEactual = gdal.Open(path + '/BLUE/' + blue[i]).ReadAsArray()      
        EVI = (NIRactual-REDactual)/(NIRactual+6*REDactual-7.5*BLUEactual+1)
        iv_saida = driver.Create(path + '/EVI/'+ 'EVI_' + out[i], shape[1], shape[0], 1, gdal.GDT_Float32)
        iv_saida.SetGeoTransform(geo) # set the datum
        iv_saida.SetProjection(proj)  # set the projection
        iv_saida.GetRasterBand(1).WriteArray(EVI) 
    return iv_saida


 
#The next line must be changed for your root folder for the RED and NIR
#files, remember, it's case sensitive
NDVI('/media/denis/DATA/Drought_tests3/',red,nir,out)
EVI('/media/denis/DATA/Drought_tests3/',red,nir,blue,out)
#NDWI('/media/denis/DATA/Drought_tests3/',nir2,nir,out)



print 'A operação de cálculo dos índices levou ', time.time() - startTime, 'segundos'
print 'Foram geradas', len(red), 'imagens para cada índice'
