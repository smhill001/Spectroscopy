# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 13:16:32 2014

@author: steven.hill

2015-02-17: Considering an update that would provide average or total
signal in a set of spectral windows when ContWidth is set to zero.
It would permit simpler band ratio analyses to be conducted that aren't
dependent on nearby continua.

"""
import sys
drive='f:'
sys.path.append(drive+'\\Astronomy\Python Play\Util')

import ConfigFiles as CF

class LineBandPhysicsList(CF.readtextfilelines):
    """
    TBD
    
    """
    pass
        
    def load_records(self,Species="All",WVRange=[350.,1050.]):
        """
        Deal with 4 use cases:
            1. Get all species, all wavelengths
            2. Get a single species, all wavelengths
            3. Get a single species, limited wavelengths
            4. Get all species, limited wavelengths
        """
        print "Hi in LineBandPhysicsList.load_records"
        
        self.Species=[]
        self.ID=[]
        self.WVCntr=[]
        self.Strength=[]
        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            print fields
            if Species=="All":
                print "WVRange, fields[2]=",WVRange, fields[2]
                if float(WVRange[0])<float(fields[2]) and float(WVRange[1])>float(fields[2]):
                    self.Species.extend([str(fields[0])])
                    self.ID.extend([str(fields[1])])
                    self.WVCntr.extend([float(fields[2])])
                    self.Strength.extend([float(fields[3])])
            else:
                if fields[0]==Species:  
                    if WVRange[0]<fields[2] and WVRange[1]>fields[2]:
                        self.Species.extend([str(fields[0])])
                        self.ID.extend([str(fields[1])])
                        self.WVCntr.extend([float(fields[2])])
                        self.Strength.extend([float(fields[3])])
        
        return 1
    
class LinesBands_to_Measure(CF.readtextfilelines):
    """
    TBD
    
    """
    pass
        
    def load_records(self,Type="All",WVRange=[350.,1050.]):
        """
        Deal with 4 use cases:
            1. Get all types, all wavelengths
            2. Get a single type, all wavelengths
            3. Get a single type, limited wavelengths
            4. Get all types, limited wavelengths
        """
        print "Hi in load_records"
        #ID,Start(nm),End(nm),ContWdth(nm)
        self.Type=[]
        self.ID=[]
        self.WV0=[]
        self.WV1=[]
        self.WVCont=[]
        
        for recordindex in range(1,self.nrecords):
            fields=self.CfgLines[recordindex].split(',')
            #print fields
            if Type=="All":
                #print "WVRange, fields[2]=",WVRange, fields[2]
                if float(WVRange[0])<float(fields[2]) and float(WVRange[1])>float(fields[3]):
                    self.Type.extend([str(fields[0])])
                    self.ID.extend([str(fields[1])])
                    self.WV0.extend([float(fields[2])])
                    self.WV1.extend([float(fields[3])])
                    self.WVCont.extend([float(fields[4])])
            else:
                if fields[0]==Type:  
                    if float(WVRange[0])<float(fields[2]) and float(WVRange[1])>float(fields[3]):
                        self.Type.extend([str(fields[0])])
                        self.ID.extend([str(fields[1])])
                        self.WV0.extend([float(fields[2])])
                        self.WV1.extend([float(fields[3])])
                        self.WVCont.extend([float(fields[4])])
        
        return 1
   
def ComputeEW1(Spectrum,Target,DateTime,BandType,BandName,BandWave1,BandWave2,ContWidth,Outfile,Append):
    
    
    import numpy as np
    import datetime
    BandIndices=np.where((Spectrum[:,0] > BandWave1) & (Spectrum[:,0] < BandWave2))
    BandMean=Spectrum[BandIndices,1].mean()
    ContIndices1=np.where((Spectrum[:,0] >BandWave1-ContWidth) & (Spectrum[:,0] < BandWave1))
    ContIndices2=np.where((Spectrum[:,0] >BandWave2) & (Spectrum[:,0] < BandWave2+ContWidth))
    ContIndices=np.concatenate((ContIndices1,ContIndices2),axis=1)
    ContMean=Spectrum[ContIndices,1].mean()
    #print "+++++",BandName,BandIndices
    BandStart=Spectrum[BandIndices,0].min()
    BandEnd=Spectrum[BandIndices,0].max()
    EW=(1.-BandMean/ContMean)*(Spectrum[BandIndices,0].max()-Spectrum[BandIndices,0].min())
    if BandStart<1500.:
        tempstring=','.join(['%.3f' % num for num in [BandStart,BandEnd,ContWidth,EW]])
    else:    
        tempstring=','.join(['%.3f' % num for num in [BandStart/10.,BandEnd/10.,ContWidth/10.,EW/10.]])
    
    #tempstring=','.join(['%.3f' % num for num in [BandStart/10.,BandEnd/10.,ContWidth/10.,EW/10.]])
    tempstring=Target+","+datetime.datetime.strftime(DateTime,'%Y-%m-%d %H:%M:%S')+","+BandType+","+BandName+","+tempstring+"\n"
    if Append:
        with open(Outfile, "a") as text_file:
            text_file.write(tempstring)
            text_file.close() 
    else:
        text_file = open(Outfile, "w")
        text_file.write(tempstring)
        text_file.close()
        
    
    return 0

class EWObservations(CF.readtextfilelines):
    pass                
    
    def load_records(self,Target="All",BandID="All"):

        print "EWObservations.load_records"

        self.TargetID=[]
        self.DateTimeUTObs=[]
        self.BandType=[]
        self.BandIdentifier=[]
        self.WV0=[]
        self.WV1=[]
        self.ContWV=[]
        self.EW=[]

        for recordindex in range(0,self.nrecords):
            #print "recordindex, FirstTime=",recordindex,FirstTime
            fields=self.CfgLines[recordindex].split(',')
            if Target=="All" or Target==fields[0]:
                if BandID=="All" or BandID==fields[3]:
                    self.TargetID.extend([fields[0]])
                    self.DateTimeUTObs.extend([fields[1]])
                    self.BandType.extend([fields[2]])
                    self.BandIdentifier.extend([fields[3]])
                    self.WV0.extend([float(fields[4])])
                    self.WV1.extend([float(fields[5])])
                    self.ContWV.extend([float(fields[6])])
                    self.EW.extend([float(fields[7])])
 
        return 0                
