# -*- coding: utf-8 -*-
"""
Created on Thu Jun 07 12:11:23 2018

@author: Steven Hill
"""

def ComputeSpectrum(FN,extendWV=False): 
    
    #Seems like mayber this should be a class with some methods!!!
    drive="f:"
    import sys    
    import numpy as np
    from astropy.io import fits
    import GeneralSpecUtils as GSU
    sys.path.append(drive+'\\Astronomy\Python Play\SpectroPhotometry\Spectroscopy')

    hdulist=fits.open(FN,mode='update')
    #print hdulist[0].header
    print "len(hdulist[0].header)=",len(hdulist[0].header)
    #
    A=FITSSpectraObject(hdulist)
    A.ComputeRawSpectralValues()
    A.CalibrateData()
    
    wavegrid,griddata=GSU.uniform_wave_grid(A.wavearray,A.data,Extend=False)
    spectrum=np.transpose(np.array([wavegrid,griddata]))

    hdulist.close()

    meta=GSU.spec_meta_data()
    meta.Filter=A.Filter
    meta.Native_Dispersion=A.wvsample
    meta.DateObs=A.DateObs
    
    return spectrum,meta

class FITSSpectraObject:
        def __init__(self,hdulist):
#def Average_Spectrum(drive,ObsList):
            import numpy as np

            temp=hdulist[0].header['FILTER']
            self.Filter=temp[0:3]
            print "Filter=",self.Filter
            self.NAXIS1=hdulist[0].header['NAXIS1']
            z='MIDPOINT' in hdulist[0].header
            if z:
                self.DateObs=np.str(hdulist[0].header['MIDPOINT'])
            else:
                self.DateObs=np.str(hdulist[0].header['DATE-OBS'])
            self.Aperture=np.float(hdulist[0].header['APERTURE'])
            self.ExpTime=np.float(hdulist[0].header['EXPTIME'])
            self.DataRow1=np.int(hdulist[0].header['DATAROW1'])
            self.DataRow2=np.int(hdulist[0].header['DATAROW2'])
            self.Bkg1Row1=np.int(hdulist[0].header['BKG1ROW1'])
            self.Bkg1Row2=np.int(hdulist[0].header['BKG1ROW2'])
            self.Bkg2Row1=np.int(hdulist[0].header['BKG2ROW1'])
            self.Bkg2Row2=np.int(hdulist[0].header['BKG2ROW2'])
            self.Pixel1=np.float(hdulist[0].header['PIXEL1'])
            self.Wave1=np.float(hdulist[0].header['WAVE1'])
            self.Pixel2=np.float(hdulist[0].header['PIXEL2'])
            self.Wave2=np.float(hdulist[0].header['WAVE2'])
            self.XPix1=np.int(hdulist[0].header['XPIX1'])
            self.XPix2=np.int(hdulist[0].header['XPIX2'])

            self.imagedata=hdulist[0].data
            
        def ComputeRawSpectralValues(self):
            import numpy as np
            
            #Compute 1D sum spectrum and clip
            self.numdatarows=self.DataRow2-self.DataRow1+1
            self.data=np.sum(self.imagedata[self.DataRow1:self.DataRow2+1,:],axis=0)
            self.data[:self.XPix1]=np.nan
            self.data[self.XPix2:]=np.nan
            
            #Compute 1D average background
            self.numBkg1rows=self.Bkg1Row2-self.Bkg1Row1+1
            self.numBkg2rows=self.Bkg2Row2-self.Bkg2Row1+1
            print "data.size",self.data.size
            if self.Bkg1Row1<0: #AH. A FLAG TO SET A FIXED BACKGROUND VALUE
                self.BkgAvg=np.ones([self.data.size])*self.Bkg1Row2
            else:
                self.Bkg1=np.sum(self.imagedata[self.Bkg1Row1:self.Bkg1Row2+1,:],axis=0)
                self.Bkg2=np.sum(self.imagedata[self.Bkg2Row1:self.Bkg2Row2+1,:],axis=0)
                self.BkgAvg=(self.Bkg1+self.Bkg2)/(self.numBkg1rows+self.numBkg2rows)
                
            #Compute wavelength sampling and array
            self.wvsample=(self.Wave2-self.Wave1)/(self.Pixel2-self.Pixel1)
            self.wvzero=self.Wave1-self.wvsample*self.Pixel1
            self.wavearray=self.wvsample*np.zeros(self.NAXIS1,1,dtype=float)+self.wvzero
            self.waveXPix1=self.wvsample*self.XPix1+self.wvzero
            self.waveXPix2=self.wvsample*self.XPix2+self.wvzero
            
        def CalibrateData(self):
                #Compute flux in terms of DN-(s^-1)-(nm^-1)-(m^2)
            if self.Bkg1Row1<0:
                self.Calibrated=self.numdatarows*(((self.data-self.BkgAvg)/self.numdatarows)/
                                            (self.ExpTime*self.wvslope*self.Aperture))
            else:
                self.Calibrated=self.numdatarows*((self.data/self.numdatarows-self.BkgAvg)/
                                            (self.ExpTime*self.wvslope*self.Aperture))
