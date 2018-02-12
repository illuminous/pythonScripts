# Import system modules
import arcgisscripting

# Create the Geoprocessor object
gp = arcgisscripting.create()

try:
    # Set local variables
    outRaster = "G://Working//Carbon//for_Jason//combo_test//burnp_CrEm"

    # Check out Spatial Analyst extension license
    gp.CheckOutExtension("Spatial")

    # Process: Combine...
    gp.Combine_sa("'G://Working//Carbon//for_Jason//combo_test//burnprob_10k';'G://Working//Carbon//for_Jason//combo_test//c_em_10k'", outRaster)

except:
    # If an error occurred while running a tool, then print the messages.
    print gp.GetMessages()
