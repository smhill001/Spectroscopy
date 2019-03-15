# -*- coding: utf-8 -*-
"""
Created on Fri Jun 08 07:25:02 2018

@author: Steven Hill
"""
def SpectrumFromFITS1(Target,PlotID,PlotType,DateUT):
    import sys
    drive='f:'
    sys.path.append(drive+'\\Astronomy\Python Play')
    sys.path.append(drive+'\\Astronomy\Python Play\Util')
    sys.path.append(drive+'\\Astronomy\Python Play\SpectroPhotometry\Spectroscopy')
    sys.path.append(drive+'\\Astronomy\Python Play\TechniquesLibrary')
    
    import ConfigFiles as CF
    import PlotUtils as PU
    import FITSSpecUtils as FSU
    import GeneralSpecUtils as GSU
    import numpy as np
    import matplotlib.pyplot as pl
    import scipy, datetime, time
    import copy
    
    rootpath="f:/Astronomy/Python Play/SpectroPhotometry/Spectroscopy/"
    TargetParams=CF.Target_Parameters(rootpath+"Target_Parameters.txt")
    PlotParams=PU.PlotSetup(rootpath+"SpecPlotConfig1.txt")
    MeasParams=CF.measurement_list(rootpath+"FITSSpectralImageList.txt")
    
    TargetParams.loadtargetparams(Target)
    PlotParams.loadplotparams(drive,PlotID,PlotType)
    PlotParams.Setup_Plot()
    MeasParams.load_records(Target,DateUT) #####
    #MeasParams.load_all_data() ## I Used this when combining multiple obs of
                                ## same target, specifically multiple observations
                                ## for filter calibration.
    
    path=CF.built_path(TargetParams) #Build path to the target FITS files
    path.spectra(DateUT)
    print "***********MeasParams.FileList=",MeasParams.FileList
    counter=0
    for f in MeasParams.FileList:
        FN=path.input_path+f
        
        spectrum,meta=FSU.ComputeSpectrum(FN,extendWV=False)
        if counter==0:
            print spectrum.shape[0]
            specarray=np.zeros((spectrum.shape[0],1),dtype=float)
            print specarray.shape
            specarray[:,0]=spectrum[:,1]
            print specarray.shape
        else:
            tmpsig=np.reshape(spectrum[:,1],(spectrum.shape[0],1))
            print spectrum.shape,tmpsig.shape
            specarray=np.append(specarray,tmpsig,axis=1)
            print specarray.shape
        counter=counter+1

        Temp=PU.Draw_with_Conf_Level(spectrum,1.0,'g',Target+'_'+meta.DateKey)
        
        pl.legend(loc=0,ncol=1, borderaxespad=0.,prop={'size':6})
        pl.subplots_adjust(left=0.10, bottom=0.14, right=0.98, top=0.92,
                    wspace=None, hspace=None)
        pl.savefig(path.One_D_path+Target+'_'+meta.DateKey+'_1D.png',dpi=300)
        np.savetxt(path.One_D_path+Target+'_'+meta.DateKey+'_1D_WVCal.txt',spectrum,delimiter=" ",fmt="%10.3F %10.7F")
        
    return specarray,spectrum,meta
