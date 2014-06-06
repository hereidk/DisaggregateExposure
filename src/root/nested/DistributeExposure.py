'''
Created on Mar 11, 2014

@author: kahere
'''

import tkinter
import tkinter.filedialog as tkFileDialog
import os
from root.nested.ClipLights import Clip, Portfolio
import numpy as np
from root.nested.EDMGenerator import EDM
import ogr
import pandas

geodatafilepath = 'C:\PF2\QGIS Valmiera\Datasets'

def countryList():
    
    choices = np.loadtxt('CountryListVShort.csv',dtype=str,delimiter=',')
    for i in range(np.size(choices)):
        choices[i] = choices[i][2:-1]
    return choices

def resolutionList():
    choices = ['Country', 'State/Province']
    return choices

def LOBList():
    choices = ['Res', 'Com']
    return choices

def perilList():
    choices = ['WS', 'EQ']
    return choices

def scrollMenu(function):
    # Drop-down menu to select country
    root = tkinter.Tk()
    root.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
    root.title('Exposure disaggregation settings')
    
    choices = function
        
    var = tkinter.StringVar(root)
    var.set(choices[0]) # Initial value
    option = tkinter.OptionMenu(root, var, *choices)
    option.pack(side='left', padx=10, pady=10)
    scrollbar = tkinter.Scrollbar(root)
    scrollbar.pack(side='right', fill='y')
    
    def get_country():
        select_country = var.get()
        root.quit()
        return select_country
    
    button = tkinter.Button(root, text='OK', command=get_country)
    button.pack(side='left', padx=20, pady=10)
        
    root.mainloop()
    country = button.invoke()
    root.withdraw()
    return country


def selectPortfolio(country):
    # Browse to directory of portfolio file
    root2 = tkinter.Tk()
    root2.withdraw()
    currdir = os.getcwd()
    validfile = False
    while validfile == False: 
        tempdir = tkFileDialog.askopenfilename(parent=root2, initialdir=currdir, title='Please select a portfolio .csv file. Cancel produces equal exposures in each state/province.')
        if len(tempdir) > 0:
#             print ('You chose %s' % tempdir)
            if tempdir.endswith('.csv'):
                portfolio_file = tempdir
                validfile = True
            else:
                print("Error: File type must be .csv.")
        else:
#             print('No portfolio file selected.')
            portfolio_file = equalExposureTestPortfolio(country)   
            validfile = True        
    return portfolio_file         

def equalExposureTestPortfolio(country):
    shp = r'%s\Boundaries\ne_10m_admin_1_states_provinces\Separated by countries\ne_10m_admin_1_states_provinces_admin__%s' % (geodatafilepath, country)
    
    DriverName = "ESRI Shapefile"
    driver = ogr.GetDriverByName(DriverName)
    shapef = driver.Open('%s.shp' % shp)
    lyr = shapef.GetLayer()
    
    province_names = np.zeros(0)
    for province in range(0,lyr.GetFeatureCount()):
        if lyr.GetFeature(province).GetField('name') != 'NULL':
            province_names = np.append(province_names,lyr.GetFeature(province).GetField('name'))
    
    portfolio_file = np.zeros((np.size(province_names),2))
    num_locs = numLocsButton()
    avg_TIV = avgTIVButton()
    portfolio_file[:,0] = num_locs
    portfolio_file[:,1] = num_locs * avg_TIV
    portfolio_file_pandas = pandas.DataFrame(portfolio_file, index = province_names, columns = ['locCount','locTIV'])
    
    file_path = '%s\%s\Provinces\%sEqualExposure.csv' % (geodatafilepath,country,country)
    portfolio_file_pandas.to_csv(file_path, columns=['locCount','locTIV'], index=True, index_label='name')
    return file_path

def generateLights(country,image_file,resolution):
    #     Generate clipped images of satellite data
    lights = Clip(country,image_file,resolution)      
    lights.clipToMask()
    
def generatePoints(country,image_file,resolution):
    # Distribute portfolio of exposures
    if resolution == 'State/Province':
        portfolio_file = selectPortfolio(country)
    if resolution == 'Country':
        numlocs = numLocsButton()
        avg_TIV = avgTIVButton()     
        portfolio_file = [country, numlocs, avg_TIV*numlocs]  
    portfolio = Portfolio(country,image_file,portfolio_file,resolution)  
    portfolio.distribute_locs()

def numLocsButton():
    root = tkinter.Tk()
    root.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
    root.title('Enter number of locations to distribute.')
      
    entry = tkinter.Entry(root)
    entry.pack()
      
    def get_country():
        var = tkinter.StringVar(root)
        select_country = var.get()
        root.quit()
        return select_country
  
    button = tkinter.Button(root, text='OK', command=get_country)
    button.pack(side='left', padx=20, pady=10)
      
    root.mainloop()
      
    numlocs = np.int(entry.get())
    root.withdraw()
    return numlocs

def avgTIVButton():
    root = tkinter.Tk()
    root.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
    root.title('Enter average TIV.')
      
    entry = tkinter.Entry(root)
    entry.pack()
      
    def get_country():
        var = tkinter.StringVar(root)
        select_country = var.get()
        root.quit()
        return select_country
  
    button = tkinter.Button(root, text='OK', command=get_country)
    button.pack(side='left', padx=20, pady=10)
      
    root.mainloop()
      
    avg_TIV = np.float(entry.get())
    root.withdraw()
    return avg_TIV

def generateEDM(country, province, LOB, peril):
    edm = EDM(country, province, LOB, peril)
    edm.genLocFile()
    edm.outputFiles()

if __name__ == '__main__':
    
    resolution = scrollMenu(resolutionList())
    country = scrollMenu(countryList())
    LOB = scrollMenu(LOBList())
    peril = scrollMenu(perilList())  
        
#     Input filename of nighttime lights dataset. If unsure, use first
#     definition of image_file, which has global coverage, but slower to run.
#     Use lights clipped to country extent to speed up code.

    image_file = r'%s\Night Lights\No-Saturation-F16_20100111-20110731_rad_v4.geotiff\No-Saturation-F16_20100111-20110731_rad_v4.geotiff\F16_20100111-20110731_rad_v4.avg_vis.tif' % geodatafilepath
#     image_file = r'C:\PF2\QGIS Valmiera\Datasets\%s\%s no saturation night lights' % (country, country)
    
    generateLights(country,image_file,resolution)
    
    generatePoints(country,image_file,resolution)    

    
#     Generate EDM file
    if resolution == 'Country':
        generateEDM(country, country, LOB, peril)
    if resolution == 'State/Province':
        province_files = os.listdir(path='%s\%s\Provinces\Points' % (geodatafilepath,country))
        for province in province_files:
            if province[:-4] != country: # Trim off '.csv', exclude full country file
                generateEDM(country, province[:-4], LOB, peril)
    
    
        