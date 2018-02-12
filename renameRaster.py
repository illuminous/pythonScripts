import arcpy
from arcpy import env

zoneres = []

eventnames = {'tmpr2':'smrtapmd2',
               'tmpr':'smortapm',
               'tmp2':'smortpmd2',
              'treem':'smortpm'}
daymetnames = {'emiss':'emissions',
               'fli':'intensity',
               'pcrown':'pcrowni',
               'pemiss':'pemission',
               'pfcons':'pfuelcon',
               'pscorch':'pscorchht',
               'psoilht':'psoilh',
               'ptrmort':'ptreem',
               'scorch':'schorchht',
               'soilht':'soilh',
               'trmort':'treem'}
def buildZones(zone_number_lower, zone_number_upper):
    for zone in range (zone_number_lower, zone_number_upper):
        if zone < 10:
            zonenum = 'z0'+'%s' %(zone)
            zoneres.append(zonenum)
        else:
            zonenum = 'z%s' %(zone)
            zoneres.append(zonenum)

def renameRaster(in_raster, out_raster):
    try:
        arcpy.Rename_management(in_raster, out_raster)
    except:pass

def main():
    buildZones(10,11)

    for zone in zoneres:
        arcpy.env.workspace = "H:/fireharmQAQC/zips/Event_Mode/%s_fh_grids" %(zone)
        datasetList = arcpy.ListDatasets("", "Raster")
        for dataset in datasetList:
            if dataset[:3] != zone:# if first 3 chars don't equal zone add the zone number on front.
                out_raster = '%s_' %(zone)+dataset
                print dataset[:3], zone
                renameRaster(dataset, out_raster)
            else:
                pass
            
            if daymetnames.has_key(dataset[4:]):
                try:
                    out_raster = '%s_%s' %(zone, daymetnames[dataset[4:]])
                    print dataset, 'switch ', out_raster
                    renameRaster(dataset, out_raster)
                except:pass
            else:
                pass

            if eventnames.has_key(dataset[4:]):
                try:
                    out_raster = '%s_%s' %(zone, eventnames[dataset[4:]])
                    print dataset, 'switch ', out_raster
                    renameRaster(dataset, out_raster)
                except:pass
            else:
                pass
            


if __name__ == '__main__':
    main()
