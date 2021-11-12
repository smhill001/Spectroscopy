# -*- codine: utf-8 -*-
"""
Created on Tue Jul 15 07:22:23 2014

@author: steven.hill

FUNCTION: SpectrumFromFITS (SpectrumFromFITS_V006.py)

This function reads spectral image data from FIT files that have been 
calibrated (bias, dark, but not necessarily flat). Using meta-data that has been 
inserted into the FITS header, data pixels and background pixels are read.  A 
linear wavelength calibration is applied and the resulting 1-dimensional spectrum
is re-gridded to standard 0.5nm wavelength intervals. Using reference spectra
(either instrument response functions or reference stellar spectra) the data
are converted to either Top of Atmosphere 'raw' fluxes or the relative 
(peak normalized to unity) response of the instrument. In addition, the
equivalent widths of lines or bands of interest are computed and written
to ASCII output files.

INPUT PARAMETERS:
    Target - This string identifies the target, e.g., "Jupiter", "Vega", etc.
             This parameter allows the lookup of the target type, e.g.,
             "Planet", "Star", etc. that permits construction of directory
             paths.
    DateUT - The UT date of the observation. Combined with Target, this forms
             a unique key to the observation, assuming that most unique parameters
             are invariant over a single observing night.
    FluxCalibration - This is a flag that determines whether the observation
             is to be processed to produce a system response (e.g. the target
             has a well defined spectrum) or if the calibrated spectrum is
             produced using a system spectral response function.
             
INPUT FILES:
    PlotParameters - List of plotting configuration info related only to the target,
             not the specific observation
    NNNNKeyFile.txt - List of Target-Date-Time keys
    ProcessingConfigFile.txt - Four parameters that control processing
    FileList - List of individual FITS files for processing
    ObsBands - List of spectral bands for which equiv. widths will be calculated
    ReferenceSpectrum - This may be a canonical reference, e.g., for a stellar
             spectral type for response computation, or it may be a response
             file
    FITS Images - 2D image files with necessary metadata for flux and wavelength
             calibration            
             
OUTPUTS:
    1D Spectrum - txt file
    1D Spectrum - png file
    1D Response or Albedo - txt file; depends on FluxCalibration flag - TBD 6/6/16
    Equivalent widths - txt file

NEXT STEPS as of 6/8/2016: (Need to verify which of these have been done)
1) Adapt this code to work multiple observations of Neptune in a single file list file.
2) Run through Neptune observations for the 2015-11-08UT and add keywords for processing
3) Close out raw and calibrated files for 11/08 so they can be zipped
4) Encapsulate target selection and associated file location meta data in
   text files and/or a python function
5) Bigger job: Make decisions on configuring EW parameters: Maybe as metadata in FITS files?
6) Make this so it full accommodates emission and reflected spectra, e.g., 
   for stars versus planets.
7) Make this so that the EWs can be calculated for either (or both?) albedo
   and/or total spectrum
8) Make smoothing of reference spectrum configurable (maybe in ProcessingConfig)
9) Provide options so that individual filter transmission can be assessed, e.g.,
   merge the Jovian Moons filter response code
10) Start using GIT?
11) Convert many functions to classes
12) Work on inheritance

"""

def SpectrumFromFITS(Target,DateUT,FluxCalibration):
    
    drive='f:'
    import sys
    sys.path.append(drive+'\\Astronomy\Python Play\SpectroPhotometry\Spectroscopy')
    sys.path.append(drive+'\\Astronomy\Python Play\SPLibraries')
    import matplotlib.pyplot as pl
    import pylab
    import numpy as np
    #import scipy
    #from PyAstronomy import pyasl #This is where the best smoothing algorithm is!
    import SpecPhotLibV006 as SPL
    import datetime
    from PyAstronomy import pyasl #This is where the best smoothing algorithm is!
    
    clrs=SPL.StarRainbow()
    plotparams=SPL.spec_plot_params(drive,Target)
    
    DataPath="/Astronomy/Projects/"+plotparams.TargetType+"/"+Target+"/Spectral Data/"
        
    ConfigFile=drive+DataPath+"Configuration Files/"+Target+DateUT+"_Config.txt"
    print "***",ConfigFile
    if Target=='TYC5811-126-1':  #Actually not sure. This star could be HD213780
        DataPath=':/Astronomy/Projects/Stellar Spectra Project 2015/TYC5811-126-1/'
        DataFileList="FileList_TYC5811-126-1_Spectra-20150913UT.txt"
        ResponseFile="/Vega/Vega_20151014025716_Response.txt"
        FluxCalibration="ApplyResponse"
    
    DataFileList,ResponseFile,FluxCalibration,ObsBandFile=SPL.GetProcessingConfig(ConfigFile)    
    
    PathName=drive+DataPath
    
    ###############################################################################
    # CREATE l1 1-D spectra from FITS files, merging VIS and NIR
    ###############################################################################  

    VFNArray,IFNArray=SPL.GetSpecObsFileNames(PathName+"Configuration Files/",DataFileList)
    print "In MAIN: VFNArray,IFNArray=",VFNArray,IFNArray
    #Compute Native dispersion from PIXEL/WAVE data in FITS Headers
    mergedspecarray,vspecarray,ispecarray,DateTimeKeyArray= \
        SPL.Make_Master_Spectrum(PathName+DateUT+"/",VFNArray,IFNArray)
    print "DateTimeKeyArray=",DateTimeKeyArray
    print "shape(VFNArray)=",np.shape(VFNArray)
    print "len(VFNArray)=",len(VFNArray)
    print "shape(mergedspecarray)=",np.shape(mergedspecarray)
    print "shape(DateTimeKeyArray)=",np.shape(DateTimeKeyArray)
    #Create Master Observed Spectrum by loading correct SINGLE row of intensity
    # into the standard 2x1895 spectral array MASTER
     #******************************************************************************
    for Obsindex in range(0,len(VFNArray)):# - this would be for multiple epochs
    # on the same DateUT
    #******************************************************************************
       
        MASTER=np.empty([1895,2])
        MASTER[:,0]=np.arange(115,1062.5,0.5,dtype=float)
        MASTER[:,1]= mergedspecarray[:,Obsindex]
        print "SpectrumFromFITS, Obsindex=",Obsindex
        np.savetxt(drive+DataPath+'1D Spectra/'+Target+DateTimeKeyArray[Obsindex]+'_1D_WVCal.txt',MASTER,delimiter=" ",fmt="%10.3F %10.7F")
        ###############################################################################
        #Do I want to pass smoothing parameters here?    
        Ref,NormResponsewithWV=SPL.GetandSmoothCalibrationSpectrum(drive,DataPath,Target,DateTimeKeyArray,
                                                           FluxCalibration,ResponseFile,MASTER)
        ###############################################################################
        print "DateTimeKeyArray=",DateTimeKeyArray                                                           
        plotparams.DateTimeKey=DateTimeKeyArray[Obsindex]
        #Begin plotting 
        #Current (10-21-2015) version just plots the first spectrum if there are more than one.
        
        #  This is where the top of a plotting loop should go. Huh?*************************
        
        #I Should pass in a string of DATETIMEKEY plus Filter for the third parameter, rather
        #  than the full file name. It will shorten the label on the legend. I could
        #  also add the exposure time and aperture if desired.
        
        first=True
        print "In SpectrumFromFITS; VFNArray[0]=",VFNArray[0]
        if VFNArray[0]<>'':
            SPL.PlotBroadBand(MASTER[:,0],vspecarray[:,Obsindex],VFNArray[Obsindex],clrs.c1[0],first,plotparams,0.5)
        first=False
        if IFNArray[0]<>'':
            SPL.PlotBroadBand(MASTER[:,0],ispecarray[:,Obsindex],IFNArray[Obsindex],clrs.c1[1],first,plotparams,0.5)
        #quit()
        #pl.plot(Ref[:,0],CLRonRef,label='CLR',linewidth=0.5)
        pl.plot(MASTER[:,0],MASTER[:,1],label='MASTER',color='k',linewidth=1)
        if FluxCalibration=="CreateResponse":
            print "Here I am"
            pl.plot(MASTER[:,0],1e6*Ref[:,1],label='Reference A0V x 1e6')
            print MASTER.size,NormResponsewithWV.size
            pl.plot(NormResponsewithWV[:,0],NormResponsewithWV[:,1]*1e6,label='Norm Response x 1e6')
        if FluxCalibration=="ApplyResponse":
            pl.plot(MASTER[:,0],plotparams.Y1*Ref[:,1]/2.0,label='System Response x'+str(plotparams.Y1/2.0))
            pl.plot(NormResponsewithWV[:,0],NormResponsewithWV[:,1],label='Calibrated',linewidth=1)
            temp=pyasl.smooth(NormResponsewithWV[:,1],3,'flat')
            pl.plot(NormResponsewithWV[:,0],temp,label='Calibrated, smoothed',linewidth=1)
            if plotparams.TargetType=="Nebulae-Planetary":
                pl.plot(NormResponsewithWV[:,0],10*NormResponsewithWV[:,1],label='10xCalibrated',linewidth=0.5)
                pl.plot(NormResponsewithWV[:,0],10*temp,label='10xCalibrated, smoothed',linewidth=1)
                pl.plot(MASTER[:,0],10*MASTER[:,1],label='10xMASTER',color='k',linewidth=0.5)
        
        EWFN=drive+DataPath+'EWs/'+Target+DateTimeKeyArray[Obsindex]+'UT-Albedo-EW.txt'
        
        #Given an ObsBandFile, load the relevant bands for a given observation
        BandNameArray,BandStartArray,BandEndArray,ContWidthArray,LabelHeightArray= \
            SPL.GetObsBands(drive+DataPath+"Configuration Files/"+ObsBandFile)
        print "***********len[BandNameArray]:",len(BandNameArray)
        for l in range(0,len(BandNameArray)):
            print "**********float(BandNameArray[l][0:3])", float(BandNameArray[l][0:3])                         
            pl.text(float(BandNameArray[l][0:3]),LabelHeightArray[l],BandNameArray[l],fontsize=6,
                verticalalignment='bottom',horizontalalignment='center',
                rotation='vertical')

        pl.legend(loc=0,ncol=1, borderaxespad=0.,prop={'size':6})
        #DISPERSION ANNOTATION
        #pl.text(700., 7e7, "Disp.: " + str(round(NativeDispersionNM,3))+" nm/pix",fontsize=6)
        #pl.text(700., 5e7, "Interp.: " + str(round(MasterDispersionNM,3))+" nm/pix",fontsize=6)
        pl.subplots_adjust(left=0.10, bottom=0.14, right=0.98, top=0.92,
                    wspace=None, hspace=None)
        
        pylab.savefig(drive+DataPath+'1D Spectra/'+Target+'_'+DateTimeKeyArray[Obsindex]+'_1D.png',dpi=300)
        
        ###############################################################################
        #COMPUTE EQUIVALENT WITDTHS OF IDENTIFIED BANDS
        ###############################################################################


        Key=Target+DateTimeKeyArray[Obsindex]
        datetimestring=DateTimeKeyArray[Obsindex]
        print "Key=",Key
        DateTime=datetime.datetime.strptime(datetimestring[0:4]+"-"+datetimestring[4:6]+"-" \
                +datetimestring[6:8]+"T"+datetimestring[8:10]+":"+datetimestring[10:12]+":"+datetimestring[12:14], \
                '%Y-%m-%dT%H:%M:%S')
        print "DateTime=",DateTime            
        
        print BandNameArray      
        print BandStartArray      
        print BandEndArray      
        print ContWidthArray      
        #print LabelHeightArray      
        
        Temp=SPL.ComputeAllEWs(MASTER,Target,DateTime,"Target",BandNameArray,
                               BandStartArray,BandEndArray,ContWidthArray,EWFN)
                                   
    return 1