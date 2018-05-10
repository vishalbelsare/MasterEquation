import importlib as port
utils=port.import_module('utils.utes')
import simulations as sim
import numpy as np
import plistlib as pll
import sys
import os

#! ==============================================================================
# JUST CHANGE THIS FILE NAME NOT THE PATHS
#^ ==============================================================================
#? ==============================================================================
runs_name = "freq_test2"
runs_num = 4
#? ==============================================================================
#^ ==============================================================================
# UNLESS YOU REALLY DGAF IM NOT YOUR DAD
#! ==============================================================================
#\\TODO: dont write so many times
#! ==============================================================================


#~ ==============================================================================
#& Making directories
#~ ==============================================================================

app_dir=os.getcwd()+'/'
results_dir=str(app_dir)+"results/"
runs_dir=str(results_dir)+runs_name+'/'
utils_dir=str(app_dir)+"utils/"
params=pll.readPlist(utils_dir+'input.data')
os.makedirs(runs_dir,exist_ok=True)
os.makedirs(utils_dir,exist_ok=True)

rates=params['rates']
a=(-5,2,2)
asw=np.logspace(a[0],a[1],a[2])
k=(-9,-6,2)
ksw=np.logspace(k[0],k[1],k[2])
for aa in asw:
    rates[0]=aa
    rates[2]=aa
    for kk in ksw:
        ext="_aa_{}_kk_{}".format(aa,kk)
        fn=runs_name+ext
        rates[4]=kk
        params['rates']=rates
        os.makedirs(runs_dir+fn+"/",exist_ok=True)
        with open(utils_dir+'input.data','wb') as f:
            pll.dump(params,f)
        with open(runs_dir+fn+"/input.data",'wb') as f:
            pll.dump(params,f)
        for i in range(1,runs_num+1):
            sim.simulation(runs_dir+fn+"/"+fn+"_"+str(i)+".json")

