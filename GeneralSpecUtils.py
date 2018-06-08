# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 14:23:24 2018

@author: Steven Hill
"""

def uniform_wave_grid(Wavelength,Signal,Extend=False):
    import numpy as np
    from scipy import interpolate
    
    if Extend:
        WaveGrid=np.arange(-100,1100,0.5,dtype=float)
    else:
        WaveGrid=np.arange(115,1062.5,0.5,dtype=float)
        
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
