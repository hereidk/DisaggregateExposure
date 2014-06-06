'''
Created on Apr 8, 2014

@author: Kelly Hereid

Modified from http://pcjericks.github.io/py-gdalogr-cookbook/layers.html
'''

from osgeo import gdal, gdalnumeric, ogr
from PIL import Image, ImageDraw
gdal.UseExceptions()
import numpy as np
import pandas
import bisect
import os
import random

geodatafilepath = 'C:\PF2\QGIS Valmiera\Datasets'

class Clip(object):
    '''
    Takes input of country, splits nighttime lights dataset by province
    '''
    
    def __init__(self, country, image_file, resolution):
        '''
        Constructor
        '''
        
        # Raster image to clip\
        self.raster = image_file
        
        # Polygon shapefile used to clip
        if resolution == 'State/Province':
            self.shp = r'%s\Boundaries\ne_10m_admin_1_states_provinces\Separated by countries\ne_10m_admin_1_states_provinces_admin__%s' % (geodatafilepath, country)
        elif resolution == 'Country':
            self.shp = r'%s\Boundaries\ne_10m_admin_0_countries\Separated by countries\ne_10m_admin_0_countries_ADMIN__%s' % (geodatafilepath, country)
        
        # Name of clip raster file(s)
        self.output = r'%s\%s\Provinces\Clip\\' % (geodatafilepath, country)
        
        # Load the source data as a gdalnumeric array
        self.srcArray = gdalnumeric.LoadFile(self.raster)
        
        # Also load as a gdal image to get geotransform 
        # (world file) info
        self.srcImage = gdal.Open(self.raster)
        
    def getResolution(self):
        geoMatrix = self.srcImage.GetGeoTransform()
        xres = geoMatrix[1]  
        yres = geoMatrix[5]
        return [xres,yres]
        
    def clipToMask(self):
        '''
        Clip raster image using shapefile outlines of provinces.
        Save results to geotiff - compatible with QGIS
        '''
        # Create an OGR layer from a boundary shapefile
        DriverName = "ESRI Shapefile"
        driver = ogr.GetDriverByName(DriverName)
        shapef = driver.Open('%s.shp' % self.shp)
        lyr = shapef.GetLayer()
        
        # Map points to pixels for drawing the 
        # boundary on a blank 8-bit, 
        # black and white, mask image.
        for province in range(0,lyr.GetFeatureCount()):
            if lyr.GetFeature(province).GetField('name') == 'NULL':
                continue
            
            geoTrans = self.srcImage.GetGeoTransform()      
            poly = lyr.GetFeature(province)
                
            minX, maxX, minY, maxY = poly.GetGeometryRef().GetEnvelope()

            ulX, ulY = self.world2Pixel(geoTrans, minX, maxY)
            lrX, lrY = self.world2Pixel(geoTrans, maxX, minY)
        
            # Calculate the pixel size of the new image
            pxWidth = int(lrX - ulX)
            pxHeight = int(lrY - ulY)
            
            clip = self.srcArray[ulY:lrY, ulX:lrX]
                    
            # Include offset to position correctly within overall image
            xoffset =  ulX
            yoffset =  ulY
            
            # Create a new geomatrix for the image
            geoTrans = list(geoTrans)
            geoTrans[0] = minX
            geoTrans[3] = maxY  
            
            # Create new mask image for each province
            rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)  
            
            geom = poly.GetGeometryRef()
            
            for ring in range(geom.GetGeometryCount()):
                points = []
                pixels = []
                geom_poly = geom.GetGeometryRef(ring)
                
                # If picking the feature gets a polygon, there are islands, 
                # go down another level to get LINEARRING
                if geom_poly.GetGeometryName() == "POLYGON":
                    pts = geom_poly.GetGeometryRef(0)
                else:
                    pts = geom.GetGeometryRef(0)
                for p in range(pts.GetPointCount()):
                    points.append((pts.GetX(p), pts.GetY(p)))
                for p in points:
                    pixels.append(self.world2Pixel(geoTrans, p[0], p[1]))
                
                rasterize = ImageDraw.Draw(rasterPoly)
                rasterize.polygon(pixels, 0)
                
                mask = self.imageToArray(rasterPoly) 
                
                
            # Clip the image using the mask
            try:
                clip = gdalnumeric.choose(mask, \
                    (clip, 0)).astype(gdalnumeric.uint32)
            except:
                print('%s exceeds the boundaries of the satellite dataset' % poly.GetField('name'))
                continue
                
            # Save clipped province image   
            province_name = poly.GetField('name')           
            gtiffDriver = gdal.GetDriverByName( 'GTiff' )
            if gtiffDriver is None:
                raise ValueError("Can't find GeoTiff Driver")
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            gtiffDriver.CreateCopy( "%s%s.tif" % (self.output, province_name),
                self.OpenArray( clip, prototype_ds=self.raster, xoff=xoffset, yoff=yoffset )
            )
        
    # This function will convert the rasterized clipper shapefile 
    # to a mask for use within GDAL.    
    def imageToArray(self,i):
        """
        Converts a Python Imaging Library array to a 
        gdalnumeric image.
        """
        a=gdalnumeric.fromstring(i.tostring(),'b')
        a.shape=i.im.size[1], i.im.size[0]
        return a
    
    def arrayToImage(self,a):
        """
        Converts a gdalnumeric array to a 
        Python Imaging Library Image.
        """
        i=Image.fromstring('L',(a.shape[1],a.shape[0]),
                (a.astype('b')).tostring())
        return i
         
    def world2Pixel(self,geoMatrix, x, y):
        """
        Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
        the pixel location of a geospatial coordinate 
        """
        ulX = geoMatrix[0]
        ulY = geoMatrix[3]
        xDist = geoMatrix[1]
        yDist = geoMatrix[5]
        pixel = int((x - ulX) / xDist)
        line = int((y - ulY) / yDist)
        return (pixel, line) 
    
    def OpenArray(self, array, prototype_ds = None, xoff=0, yoff=0 ):
        ds = gdal.Open( gdalnumeric.GetArrayFilename(array) )
    
        if ds is not None and prototype_ds is not None:
            if type(prototype_ds).__name__ == 'str':
                prototype_ds = gdal.Open( prototype_ds )
            if prototype_ds is not None:
                gdalnumeric.CopyDatasetInfo( prototype_ds, ds, xoff=xoff, yoff=yoff )
        return ds
        
    
class Portfolio(object):
    '''
    Take aggregate portfolio data, split by province, distribute
    by weighted probability using nighttime lights data
    '''
    def __init__(self,country,image_file,portfolio_file,resolution):
        if resolution == 'State/Province':
            portfile = pandas.read_csv(portfolio_file,sep=",",usecols = (0,1,2),encoding='latin-1')
        elif resolution == 'Country':
            portfile = np.reshape(portfolio_file,(1,3))
        self.portfile = np.array(portfile)
        self.country = country
        self.resolution = resolution

        # Polygon shapefile used to clip
        if resolution == 'State/Province':
            self.shp = r'%s\Boundaries\ne_10m_admin_1_states_provinces\Separated by countries\ne_10m_admin_1_states_provinces_admin__%s' % (geodatafilepath, country)
        elif resolution == 'Country':
            self.shp = r'%s\Boundaries\ne_10m_admin_0_countries\Separated by countries\ne_10m_admin_0_countries_ADMIN__%s' % (geodatafilepath, country)
        
        
        Nightlights = Clip(country,image_file,resolution)
        [self.xres,self.yres] = Nightlights.getResolution()
               
       
    def distribute_locs(self): 
        
        # Create an OGR layer from a boundary shapefile
        DriverName = "ESRI Shapefile"
        driver = ogr.GetDriverByName(DriverName)
        shapef = driver.Open('%s.shp' % self.shp)
        lyr = shapef.GetLayer()
        
        province_names = self.portfile[:,0]
        cnt = self.portfile[:,1]
        loc_count = dict(zip(province_names,cnt.astype(int)))
        loc_TIV = dict(zip(province_names,self.portfile[:,2]))
        for province in province_names:
            lyr.SetAttributeFilter("name = '%s'" % province)
            poly = lyr.GetNextFeature()
            
            # Get extent of polygon for country/state/province
            try:
                minX, maxX, minY, maxY = poly.GetGeometryRef().GetEnvelope()
            except: # Check for province name not matching shapefile data
                print("Invalid province name: ",province)
                continue
            
            # Load clipped light image file
            try:
                provArray = gdalnumeric.LoadFile(r'%s\%s\Provinces\Clip\%s.tif' % (geodatafilepath, self.country,province))
            except: # Check for image file not being produced
                print("Invalid province name: ",province)
                province = input("Please input correct province name, or None if not available. ")
                if province == 'None' or province == 'none':
                    continue
                provArray = gdalnumeric.LoadFile(r'%s\%s\Provinces\Clip\%s.tif' % (geodatafilepath, self.country,province))
            
            # Calculate average value per location
            if self.resolution == 'State/Province':
                avg_TIV = np.float(loc_TIV[province])/loc_count[province]
            elif self.resolution == 'Country':
                avg_TIV = np.float(self.portfile[0,2])/np.float(self.portfile[0,1])
            
            # Produce weighted distribution
            cumdist = list(self.accumulate(provArray.flat))
            
            # Check for light data not existing - generally uninhabited islands, etc.
            if np.max(cumdist) == 0:
                print(province, "does not have any available light data.")
                continue
            
            # Weighted distribution of lat/lon, randomly distributed within ~1km grid resolution
            # Add some variability to average TIV - need to refine with better data.
            loc = np.zeros((loc_count[province],2))
            locdist = np.zeros((loc_count[province],3))
            for i in range(loc_count[province]):
                loc[i,:] = self.setpt(provArray,cumdist,minX, minY, maxX, maxY)
                locdist[i,1] = loc[i,1] - random.random() * self.xres
                locdist[i,0] = loc[i,0] + random.random() * self.yres
                locdist[i,2] = np.random.normal(loc=avg_TIV,scale=avg_TIV/10.) # Note: refine std dev est
    
            # Scale randomly-produced insured values to match known total for region    
            sum_TIV = np.sum(locdist[:,2])
            scale_TIV = np.float(loc_TIV[province])/sum_TIV
            locdist[:,2] = locdist[:,2] * scale_TIV
                           
            # Output latitude, longitude, total insured value to .csv file
            output = r'%s\%s\Provinces\Points' % (geodatafilepath, self.country)
            if not os.path.exists(output):
                os.makedirs(output)
            locdist_pandas = pandas.DataFrame(locdist, columns = ['Lat','Lon','TIV'])
            locdist_pandas.to_csv('%s\%s.csv' % (output,province), columns=['Lat','Lon','TIV'], index=False)
            
    def setpt(self,zd,cumdist,x0,y0,x1,y1):
        '''
        Randomly place points based on cumulative distribution (weighted probability)
        '''
        scale = 1
        x = random.random() * cumdist[-1]
        loc = range(0,len(zd.flat))
        startpt = loc[bisect.bisect(cumdist, x)]
        w = float(np.shape(zd)[1] * scale)
        startlat = np.floor((startpt/w))*self.yres/scale+float(y1)
        startlon = startpt%w/scale*self.xres+float(x0)
        startpt = [startlat, startlon]
        return startpt
    
    def accumulate(self,iterable):
        'Return running totals'
        # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
        it = iter(iterable)
        total = int(next(it))
        yield total
        for element in it:
            total = total + int(element)
            yield total
            