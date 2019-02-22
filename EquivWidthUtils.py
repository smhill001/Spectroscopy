# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 13:16:32 2014

@author: steven.hill

2015-02-17: Considering an update that would provide average or total
signal in a set of spectral windows when ContWidth is set to zero.
It would permit simpler band ratio analyses to be conducted that aren't
dependent on nearby continua.

"""
class EWBandList(CF.readtextfilelines):
    """
    TBD
    
    """
    pass
    def loadEWBands(self):
#Type,ID,Label,Species,WVCntr,WV1,WV2,WVCont,Strgth,
        FirstTime=True
        self.Type=[]
        self.ID=[]
        self.Label=[]
        self.Species=[]
        self.WVCntr=[]
        self.WV1=[]
        self.WV2=[]
        self.WVCont=[]
        self.Strgth[]
        self.NObs=0
        
        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            self.ObjectIdentifierDD.extend([str(fields[0])])
            self.Cont_Flag.extend([str(fields[1])])
            self.RAJ2000.extend([float(fields[2])])
            self.DEJ2000.extend([float(fields[3])])
            self.X.extend([float(fields[4])])
            self.Y.extend([float(fields[5])])
            self.Label_Flag.extend([str(fields[6])])
            self.Info.extend([str(fields[7])])
            self.NObs=self.NObs+1
        print self.NObs

class measurement_list(CF.readtextfilelines):
    pass
    def load_all_data(self):
        print "Hi in measurement_list>load_all_data"
        self.MeasTarget=['']   #Keyword for star identification
        self.DataType=['']           #Target, e.g., component of a multiple star
        self.DataTarget=['']           #Target, e.g., component of a multiple star
        self.DateUT=['']           #UT Date of observation: YYYYMMDDUT
        self.Optics=['']       #Instrument code, to be used for aperture
        self.Camera=['']       #Instrument code, to be used for aperture
        self.Grating=['']    #Grating 100lpm or 200lpm or None
        self.FileList=['']         #List of observation image files (FITS)
        self.NObs=0               #Number of observatinos
        FirstTime=True

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            if FirstTime:
                self.MeasTarget[0]=str(fields[0])
                self.DataType[0]=str(fields[1])
                self.DataTarget[0]=str(fields[2])
                self.DateUT[0]=str(fields[3])
                self.Optics[0]=str(fields[4])
                self.Camera[0]=str(fields[5])
                self.Grating[0]=str(fields[6])
                self.FileList[0]=str(fields[7])
                FirstTime=False
                self.NObs=1
            else:
                self.MeasTarget.extend([str(fields[0])])
                self.DataType.extend([str(fields[1])])
                self.DataTarget.extend([str(fields[2])])
                self.DateUT.extend([str(fields[3])])
                self.Optics.extend([str(fields[4])])
                self.Camera.extend([str(fields[5])])
                self.Grating.extend([str(fields[6])])
                self.FileList.extend([str(fields[7])])
                self.NObs=self.NObs+1

    def load_select_data(self,MeasTgt,DateUTSelect="All"):
        
        self.MeasTarget=['']   #Keyword for star identification
        self.DataType=['']           #Target, e.g., component of a multiple star
        self.DataTarget=['']           #Target, e.g., component of a multiple star
        self.DateUT=['']           #UT Date of observation: YYYYMMDDUT
        self.Optics=['']       #Instrument code, to be used for aperture
        self.Camera=['']       #Instrument code, to be used for aperture
        self.Grating=['']    #Grating 100lpm or 200lpm or None
        self.FileList=['']         #List of observation image files (FITS)
        self.NObs=0                #Number of observatinos
        FirstTime=True

        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            if fields[0]==MeasTgt:
                if DateUTSelect=="All":
                    if FirstTime:
                        self.MeasTarget[0]=str(fields[0])
                        self.DataType[0]=str(fields[1])
                        self.DataTarget[0]=str(fields[2])
                        self.DateUT[0]=str(fields[3])
                        self.Optics[0]=str(fields[4])
                        self.Camera[0]=str(fields[5])
                        self.Grating[0]=str(fields[6])
                        self.FileList[0]=str(fields[7])
                        FirstTime=False
                        self.NObs=1
                    else:
                        self.MeasTarget.extend([str(fields[0])])
                        self.DataType.extend([str(fields[1])])
                        self.DataTarget.extend([str(fields[2])])
                        self.DateUT.extend([str(fields[3])])
                        self.Optics.extend([str(fields[4])])
                        self.Camera.extend([str(fields[5])])
                        self.Grating.extend([str(fields[6])])
                        self.FileList.extend([str(fields[7])])
                        self.NObs=self.NObs+1
                else:
                    if DateUTSelect==fields[3]:
                        if FirstTime:
                            self.MeasTarget[0]=str(fields[0])
                            self.DataType[0]=str(fields[1])
                            self.DataTarget[0]=str(fields[2])
                            self.DateUT[0]=str(fields[3])
                            self.Optics[0]=str(fields[4])
                            self.Camera[0]=str(fields[5])
                            self.Grating[0]=str(fields[6])
                            self.FileList[0]=str(fields[7])
                            FirstTime=False
                            self.NObs=1
                        else:
                            self.MeasTarget.extend([str(fields[0])])
                            self.DataType.extend([str(fields[1])])
                            self.DataTarget.extend([str(fields[2])])
                            self.DateUT.extend([str(fields[3])])
                            self.Optics.extend([str(fields[4])])
                            self.Camera.extend([str(fields[5])])
                            self.Grating.extend([str(fields[6])])
                            self.FileList.extend([str(fields[7])])
                            self.NObs=self.NObs+1
                    


def ComputeEW(Spectrum,BandName,BandWave1,BandWave2,ContWidth,Outfile,Append):
    
    import numpy as np
    BandIndices=np.where((Spectrum[:,0] > BandWave1) & (Spectrum[:,0] < BandWave2))
    BandMean=Spectrum[BandIndices,1].mean()
    ContIndices1=np.where((Spectrum[:,0] >BandWave1-ContWidth) & (Spectrum[:,0] < BandWave1))
    ContIndices2=np.where((Spectrum[:,0] >BandWave2) & (Spectrum[:,0] < BandWave2+ContWidth))
    ContIndices=np.concatenate((ContIndices1,ContIndices2),axis=1)
    ContMean=Spectrum[ContIndices,1].mean()
    BandStart=Spectrum[BandIndices,0].min()
    BandEnd=Spectrum[BandIndices,0].max()
    EW=(1.-BandMean/ContMean)*(Spectrum[BandIndices,0].max()-Spectrum[BandIndices,0].min())
    if BandStart<1500.:
        tempstring=','.join(['%.3f' % num for num in [BandStart,BandEnd,ContWidth,EW]])
    else:    
        tempstring=','.join(['%.3f' % num for num in [BandStart/10.,BandEnd/10.,ContWidth/10.,EW/10.]])
        
    tempstring=BandName+","+tempstring+"\n"
    if Append:
        with open(Outfile, "a") as text_file:
            text_file.write(tempstring)
            text_file.close() 
    else:
        text_file = open(Outfile, "w")
        text_file.write(tempstring)
        text_file.close()
        
    
    return BandName,BandStart,BandEnd,ContWidth,EW



###############################################################################
def GetBandData(drive,BandType):
    
    CfgFile=open(drive+"/Astronomy/Python Play/SPLibraries/"+BandType+".txt",'r')
    CfgLines=CfgFile.readlines()
    CfgFile.close()
    nrecords=len(CfgLines)
    print ""
    print "GetBandData: CfgLines,nrecords",CfgLines,nrecords
    print ""
    BandIDArray=['']
    BandWVArray=[0]
    BandStrArray=[0]
    FirstTime=True
    for recordindex in range(1,nrecords):
        fields=CfgLines[recordindex].split(',')
        #print "recordindex,fields=",recordindex,fields
        if FirstTime:
            BandIDArray[0]=str(fields[0])
            #print "float(fields[1])=",float(fields[1])
            BandWVArray[0]=float(fields[1])
            BandStrArray[0]=float(fields[2])
            FirstTime=False
        else:
            BandIDArray.extend([str(fields[0])])
            BandWVArray.extend([float(fields[1])])
            BandStrArray.extend([float(fields[2])])
            
    if BandType == "Methane VIS":
        BandIDArray=["CH4 5430","CH4 6190","CH4 7050","CH4 7250"]
        BandWVArray=[543.,619.,705.,725.]
        BandStrArray=[29.8,131.8,51.0,771.] #6680 band strength is placeholder only
    elif BandType == "Methane VIS2": #Titan
        BandIDArray=["CH4 5430","CH4 5760","CH4 6190","CH4 7050","CH4 7250"]
        BandWVArray=[543.,576.,619.,705.,725.]
        BandStrArray=[29.8,15.0,131.8,51.0,771.]
    elif BandType=="Neptune Methane VIS NEW":
        BandIDArray=["CH4 4410","CH4 4590","CH4 4860","CH4 5090","CH4 5430",
                   "CH4 5760","CH4 5970","CH4 6190","CH4 6680","CH4 6825",
                   "CH4 7050","CH4 7250"]
        BandWVArray=[441.0,459.0,486.0,509.0,543.0,
                     576.0,597.0,619.0,668.0,682.5,
                     705.0,725.0]
        BandStrArray=[1.7,999.0,6.0,999.0,29.8,
                      15.0,999.0,131.8,999.0,6.9,
                      51.0,771.0] #6680 band strength is placeholder only
        StartWVArray=[436.0,450.0,470.0,498.0,525.0,
                      559.0,586.0,603.0,640.0,681.0,
                      690.0,708.0]
        EndWVArray=[446.0,464.0,492.0,516.0,552.0,
                    586.0,602.0,633.0,677.0,688.0,
                    707.0,748.0]               
        ContWidthArray=[2.,3.,3.,3.,2.,
                        3.,3.,2.,2.,2.,
                        2.,3.]            

    elif BandType == "Methane NIR":
        BandIDArray=["CH4/NH3? 7900","CH4 8420","CH4 8620","CH4 8890"]
        BandWVArray=[790.,842.,862.,889.]
        BandStrArray=[363.3,114.,823.,5753.]
    elif BandType == "Methane NIR1": #Neptune
        BandIDArray=["CH4 6825","CH4 7050","CH4 7250","CH4/NH3? 7900"]
        BandWVArray=[683.,705.,725.,790.]
        BandStrArray=[6.9,51.0,771.,363.3]
    elif BandType == "Methane NIR2": #Titan?
        BandIDArray=["CH4/NH3? 7900","CH4 8420","CH4 8890"]
        BandWVArray=[790.,842.,889.]
        BandStrArray=[363.,114.,5753.]
    elif BandType == "Solar Calcium":
        BandIDArray=["Ca II H&K","Ca I 'g band'","Ca II 8498","Ca II 8542","Ca II 8662"]
        BandWVArray=[393.,396.,850.,854.,866.]
        BandStrArray=[1.,1.,1.,1.,1.]
    elif BandType == "Solar Iron":
        BandIDArray = ["Fe 3820","Fe I 'd band'","Fe I 5270"]
        BandWVArray=[382.,438.,527.] #Not sure about Fe I d band
        BandStrArray=[1.,1.,1.]
    elif BandType == "Solar Metals":
        BandIDArray=["G band 4300","Mg 5170","Na D"]
        BandWVArray=[430.,517.,589.]
        BandStrArray=[1.,1.,1.]
        
    return BandIDArray,BandWVArray,BandStrArray
    
def GetBandTypes(drive,Target,TargetType,SpectrumType):
    #Still need to migrate this to a TargetEWPlotConfig.txt file
    #Vega already has an example *.txt file created, but I don't think
    #any code is written to read it.
    """TargetDataPath= drive+"/Astronomy/Projects/"+TargetType+"/"+Target+"/Spectral Data/Config Files/"
    CfgFile=open(TargetDataPath+Target+"_EWPlotConfig.txt",'r')
    CfgLines=CfgFile.readlines()
    CfgFile.close()
    nrecords=len(CfgLines)
    print "CfgLines,nrecords",CfgLines,nrecords
    print ""
    BandIDArray=['']
    BandWVArray=[0]
    BandStrArray=[0]
    FirstTime=True
    for recordindex in range(1,nrecords):
        fields=CfgLines[recordindex].split(',')
        print "recordindex,fields=",recordindex,fields
        if FirstTime:
            BandIDArray[0]=str(fields[0])
            print "float(fields[1])=",float(fields[1])
            BandWVArray[0]=float(fields[1])
            BandStrArray[0]=float(fields[2])
            FirstTime=False
        else:
            BandIDArray.extend([str(fields[0])])
            BandWVArray.extend([float(fields[1])])
            BandStrArray.extend([float(fields[2])])"""
            


    if SpectrumType=="RawFlux"and Target=="Jupiter":
        BandTypesAllowed=["HI Balmer","Solar Calcium","Solar Iron","Solar Metals","O2 Telluric",
                         "Telluric H2O","Methane VIS","Methane NIR"]    
    if SpectrumType=="Albedo"and Target=="Jupiter":
        BandTypesAllowed=["Methane VIS","Methane NIR"]    
    if SpectrumType=="Albedo" and Target=="Titan":
        BandTypesAllowed=["Methane VIS2"]  
    if SpectrumType=="Albedo" and Target=="Uranus":
        BandTypesAllowed=["Methane VIS1","Methane NIR1"]    
    if SpectrumType=="Albedo" and Target=="Neptune":
        BandTypesAllowed=["CH4_VIS1","CH4_NIR1"]    
    if SpectrumType=="Albedo" and Target=="Vega":
        BandTypesAllowed=["HI Balmer","O2 Telluric","H2O Telluric","HI Paschen"]    
    if SpectrumType=="Albedo" and Target=="NGC7009":
        BandTypesAllowed=["HI Balmer"]    
    if SpectrumType=="Albedo" and Target=="BetLyr":
        BandTypesAllowed=["HI Balmer","O2 Telluric","H2O Telluric"]    
        
    return BandTypesAllowed
