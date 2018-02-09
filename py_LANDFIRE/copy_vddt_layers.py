import os,shutil,sys

Zones=['03','05','06','10','12','13','14','16','17','18','19','23','24']
for Zone in Zones:
    outdir="k:/fe/landfire/dat3/firereg/z%s/dat/gis_data/gis_fin"%(Zone)
    zonedir="k:/fe/landfire/dat3/firereg/z%s"%(Zone)
    gis_dir="//Pcde6y01441/landsum/z%s/gis_data"%(Zone)
    amlfilename="c:/temp/copy_vddt_layers.aml"


    amldata = """
    ECHO ON
    &sv zone = %s
    &sv zonedir = %s
    &sv indir = %s
    &sv outdir = %s

    w %%zonedir%%
    &if [ exists %%outdir%% -directory] &then	
            &type **gis_fin folder is there**
            &else
            cw K:\fe\landfire\dat3\firereg\z%%zone%%\gis\gis_fin
            
    w %%indir%%

    &if [ exists %%indir%%\z%%zone%%_vfrg -grid] &then
            &if [exists %%outdir%%\z%%zone%%_vfrg -grid] &then kill %%outdir%%\z%%zone%%_vfrg all
            &type **copying vfrg**
            copy z%%zone%%_vfrg %%outdir%%\z%%zone%%_vfrg
    &if [ exists %%indir%%\z%%zone%%_vfri -grid] &then
            &if [exists %%outdir%%\z%%zone%%_vfri -grid] &then kill %%outdir%%\z%%zone%%_vfri all
            &type **copying vfri**
            copy z%%zone%%_vfri %%outdir%%\z%%zone%%_vfri
    &if [ exists %%indir%%\z%%zone%%_vfrcc -grid] &then
            &if [exists %%outdir%%\z%%zone%%_vfrcci -grid] &then kill %%outdir%%\z%%zone%%_vfrcc all
            &type **copying vfrcc**
            copy z%%zone%%_vfrcc %%outdir%%\z%%zone%%_vfrcc
    &if [ exists %%indir%%\z%%zone%%_vdep -grid] &then
            &if [exists %%outdir%%\z%%zone%%_vdep -grid] &then kill %%outdir%%\z%%zone%%_vdep all
            &type **copying vdep**
            copy z%%zone%%_vdep %%outdir%%\z%%zone%%_vdep 
    """%(Zone,zonedir,gis_dir,outdir)

    amlfile=open(amlfilename,'w')
    amlfile.write(amldata)
    amlfile.close()
    #now run it!
    arc='C:/arcgis/arcexe9x/bin/arc.exe'
    args=['arc',"&r %s"%(amlfilename)]
    os.spawnv(os.P_WAIT,arc,args)
