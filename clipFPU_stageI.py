import arcgisscripting
gp = arcgisscripting.create()
gp.OverWriteOutput = 1



fpus = ['CA_CA', 'EA_IA', 'EA_IL', 'EA_IN','EA_MI', 'EA_MN', 'EA_MO',
'EA_NH', 'EA_NJ', 'EA_OH', 'EA_PA', 'EA_WI', 'EA_WV', 'GB_ID', 'GB_NV',
'GB_UT', 'GB_WY', 'NR_ID','NR_MT', 'NR_ND', 'NW_OR', 'NW_WA', 'RM_CO',
'RM_KS', 'RM_NE', 'RM_SD', 'RM_WY', 'SA_AL', 'SA_AR', 'SA_FL', 'SA_GA',
'SA_KY', 'SA_LA', 'SA_MD','SA_MS', 'SA_NC', 'SA_OK', 'SA_SC', 'SA_TN',
'SA_TX', 'SA_VA', 'SW_AZ', 'SW_NM', 'SW_TX'] #these are FPUs

ext = ['_001','_002', '_003', '_004', '_005', '_006', '_007', '_008', '_009', '_010', '_011', '_012', '_013', '_014', '_015']
split = ['0','1', '2']
def clipFeature(in_features, clip_features, out_feature):
    try:
        # Process: Clip the vegetation feature class to stream_crossing_100m
        gp.Clip_analysis(in_features, clip_features, out_feature)
    except:
        # If an error occurred while running a tool print the messages
        print gp.GetMessages()



def main():
    for fpu in fpus:
        print fpu
        for x in ext:
            print x
            for s in split:
                gp.Workspace = ("F:/landcover/FPU_fSim.gdb")
                
                ##clipFeature('%s%s_TREATMENTS_Perims_%s'%(fpu, x, s), '%s%s' %(fpu, x), '%s%s_%s' %(fpu, x, s))
                
                clipFeature('%s%s_STANDARD_Perims_%s'%(fpu, x, s), '%s%s' %(fpu, x), '%s%s_%s' %(fpu, x, s))
    
