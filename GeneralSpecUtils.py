# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 14:23:24 2018

@author: Steven Hill
"""

import sys 
drive="f:"
sys.path.append(drive+'\\Astronomy\Python Play\Utils')

import ConfigFiles as CF

def uniform_wave_grid(Wavelength,Signal,Extend=False):
    import numpy as np
    from scipy import interpolate

    if Extend:
        WaveGrid=np.arange(-100,1100,0.5,dtype=float)
    else:
        WaveGrid=np.arange(115,1062.5,0.5,dtype=float)
    #print Wavelength.size,Signal.size    
    Interp=interpolate.interp1d(Wavelength,Signal,kind='linear', 
                                copy=True,bounds_error=False, 
                                fill_value=np.NaN,axis=0)  
    SignalonGrid=Interp(WaveGrid)

    return WaveGrid,SignalonGrid

def SpectrumMath(Spectrum1,Spectrum2,Operation):
    from copy import deepcopy
    import numpy as np
    ResultSpectrum=deepcopy(Spectrum1)
    if Operation == "Divide":
        ResultSpectrum[:,1]=Spectrum1[:,1]/Spectrum2[:,1]
    elif Operation == "Multiply":
        ResultSpectrum[:,1]=Spectrum1[:,1]*Spectrum2[:,1]
    #Combine uncertainty arrays in quadrature
    if Spectrum1.shape[1]==4 and Spectrum2.shape[1]==4:
        ResultSpectrum[:,2]=ResultSpectrum[:,1]*np.sqrt((Spectrum1[:,2]/Spectrum1[:,1])**2+
            (Spectrum2[:,2]/Spectrum2[:,1])**2,)
        ResultSpectrum[:,3]=ResultSpectrum[:,1]*np.sqrt((Spectrum1[:,3]/Spectrum1[:,1])**2+
            (Spectrum2[:,3]/Spectrum2[:,1])**2,)
        
    return ResultSpectrum

class spec_meta_data:
    def __init__(self):
        
        self.Filter=""
        self.Native_Dispersion=0.
        self.DateObs=""

class SpectrumAggregation:
    def __init__(self,drive,ObsList):
#def Average_Spectrum(drive,ObsList):
        import sys
        sys.path.append(drive+'\\Astronomy\Python Play\Techniques Library')
        import numpy as np
        import scipy
        import SysRespLIB as SRL
        self.path=drive+"/Astronomy/Python Play/TechniquesLibrary/"
        #print path
        for i in range(0,len(ObsList.FileList)):
            print "******** i=",i,ObsList.FileList[i]
            X=CF.ObsFileNames(ObsList.FileList[i])
            X.GetFileNames()
            print X.FNArray
            self.FNList=X.FNArray
            print "********X.FNArray",len(X.FNArray),X.FNArray
            if ObsList.DataType[i]=="Reference":
                path=drive+"/Astronomy/Python Play/SPLibraries/SpectralReferenceFiles/ReferenceLibrary/"
            else:    
                path=drive+"/Astronomy/Projects/"+ObsList.DataType[i]+"/"+ObsList.DataTarget[i]+"/Spectral Data/1D Spectra/"
            
            ###Need loop over data files here!!! "j"
            for j in range(0,len(self.FNList)):
                print "****** j=",j
                if ObsList.DataType[i]=="Reference":
                    temp2 = scipy.loadtxt(path+self.FNList[j], dtype=float, usecols=(0,1))
                else:
                    temp1 = scipy.fromfile(file=path+self.FNList[j], dtype=float, count=-1, sep='\t')    
                    temp2 = scipy.reshape(temp1,[temp1.size/2,2])
                self.wave = temp2[:,0]
                tmpsig=temp2[:,1]
                print i
                print temp2.shape
        
                if i==0 and j==0:
                    self.signalarray=np.zeros([tmpsig.size,1])
                    print self.signalarray.shape
                    self.signalarray[:,0]=tmpsig
                else:
                    print "i>0 self.signalarray.shape:",self.signalarray.shape
                    print "temp2.shape: ",temp2.shape
                    print "temp2[0,0]: ",temp2[0,0]
                    self.signalarray=np.insert(self.signalarray,1,tmpsig,axis=1)
                    print "i>0 self.signalarray.shape:",self.signalarray.shape
        if ObsList.DataType[i]=="Reference":
            self.wave=self.wave/10.

    def ComputeAverageandStats(self):
        import scipy.stats as ST
        import numpy as np
        ZeroIndices=np.where(self.signalarray <= 0.)
        self.signalarray[ZeroIndices]=np.nan
        AvgSignal=np.nanmean(self.signalarray,axis=1)
        std=np.nanstd(self.signalarray,axis=1) 
        sem=ST.sem(self.signalarray,axis=1,ddof=0,nan_policy='omit')
            
        self.MeanSpec=np.zeros([self.wave.size,4])
        self.MeanSpec[:,0]=self.wave
        self.MeanSpec[:,1]=AvgSignal
        self.MeanSpec[:,2]=std
        self.MeanSpec[:,3]=sem
        
        return 0
    
