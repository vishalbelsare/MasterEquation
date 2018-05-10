import importlib as port
utils=port.import_module('utils.utes')
import statevector as sv
k=port.import_module('kernels')
import KMC
import sys
import os
from shutil import copyfile


from astropy.table import Table, Column
import copy

def simulation(fn):
    newpath=fn 
    #path=utils.wd()+'/results/'+fn+'/'
    params=utils.load_config(utils.wd()+'/utils/input.data')
    #os.makedirs(path,exist_ok=True)
    #copyfile(utils.wd()+'/utils/input.data',path+'_input.data')
    rates=params['rates']
    proteins=params['proteins']
    nc=proteins['nucleus']
    #FINISH output_files=params['simulation']['outputs']
    MM=proteins['monomers']
    M=k.Monomers(MM)
    global x
    x=sv.StateVector(M(),delete_zeros=True)
    global model
    model=KMC.Model(x,nc)
    
    add=k.MonAdd(rates[0],M=MM,c=proteins['concentration']['value'])
    sub=k.MonSub(rates[1])
    coag=k.Coag(rates[2],M=MM,c=proteins['concentration']['value'])
    frag=k.Frag(rates[3])
    nuc=k.Nuc(rates[4],nc=nc,M=MM,c=proteins['concentration']['value'])
    
    
    # print(x)
    model.add_propensity(add)
    model.add_propensity(sub)
    model.add_propensity(nuc)
    model.add_propensity(frag)
    model.add_propensity(coag)
    model.add_mechanisms(sv.SmoluchowskiModel(x,nc))
    # print(model.mechanisms)
    X=[]
    Y=[]
    
    looping=True
    countr=0
    while(looping):
        X.append(x)
        countr+=1
        model.calculate_probability()
        model.choose()
        model.time_step()
        model.advance()
        # print(x)
        #inp=input("0 to quit: ")
        # if inp=="0":
        #     looping=False
        # if inp=="1":
        #     print(model.data)
        if countr>300:
            looping = False
        X.append(model.data)
    Y.append(X[:])
    
    
    # model.data.save(utils.wd()+'/results/'+fn+'/'+fn+str(i)+'.json',model.data_list)
    
    model.save(newpath)
    x=sv.StateVector([500],delete_zeros=True)
    model=KMC.Model(x,3)
    model.add_propensity(add)
    model.add_propensity(sub)
    model.add_propensity(nuc)
    model.add_propensity(frag)
    model.add_propensity(coag)
    model.add_mechanisms(sv.SmoluchowskiModel(x,3))
    return Y

if __name__=='__main__':
    simulation('.')

