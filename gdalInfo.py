import gdal
from gdalconst import *
filename = 'C:/fireharm/z10/z10_fin_grids/crowni'
dataset = gdal.Open( filename, GA_ReadOnly )
if dataset is None:
    pass

def printBasic(dataset):
    print 'Dataset: ', filename
    
    print 'Driver: ', dataset.GetDriver().ShortName,'/', \
          dataset.GetDriver().LongName
    
    print 'Size is ',dataset.RasterXSize,'x',dataset.RasterYSize, \
          'x',dataset.RasterCount
    
    print 'Projection is ',dataset.GetProjection()
    print 'RasterCount is ', dataset.RasterCount
    print dataset.GetGCPCount()
    geotransform = dataset.GetGeoTransform()
    if not geotransform is None:
        print 'Origin = (',geotransform[0], ',',geotransform[3],')'
        print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
    band = dataset.GetRasterBand(1)
    
def main():
    printBasic(dataset)

if __name__ == "__main__":
    main()
