import os
import FLM_stageIII
import FLM_stageIV
import FLM_stageV
import FLM_stageVI

FLM_stageIII.buildDirectories(1,100)
FLM_stageIII.combineLandfire()
FLM_stageIV.export_csvfiles()
FLM_stageV.combosToAccess()
FLM_stageVI.csvToDbase()
