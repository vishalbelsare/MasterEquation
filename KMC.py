import numpy as np
import numpy.matlib as mat
import numpy.random as npr
import statevector as sv
import kernels2 as k
from abc import ABCMeta, ABC, abstractmethod
from collections import MutableMapping
import itertools as itt
import functools as funcs
from functools import reduce
from operator import mul
import pandas as pd
import copy
from astropy.table import Table, Column
import pickle

class DataPoint:
    def __init__(self, val, t=0.0, val_unit='', t_unit='s'):
        self.point=val
        self.t=t
        self.units=(val_unit,t_unit)
    def __repr__(self):
        return '{} {} at {} {}'.format(self.point,self.units[0],self.t,self.units[1])
    def __str__(self):
        return '({},{})'.format(self.point,self.t)
    def __getitem__(self, index):
        try:
            assert((index==0 or index==1 or index==2))
            if index==0:
                return self.point
            elif index==1:
                return self.t
            else:
                return (self.point,self.t)
        except:
            raise IndexError('index can only ever be 0, 1 or 2')
    def __setitem__(self, index, val):
        try:
            assert((index==0 or index==1 or index==2))
            if index==0:
                self.point=val
            elif index==1:
                self.t=val
            else:
                try:
                    self.point=val[0]
                    self.t=val[1]
                except:
                    raise ValueError('input must be tuple or list of at least length 2')
        except:
            raise IndexError('index can only ever be 0, 1 or 2')
    def __delitem__(self, index):
        pass
    
class StateVariable(DataPoint):
    _ID=0
    @classmethod
    def get_id(cls):
        __id=copy.copy(cls._ID)
        cls._ID+=1
        return __id
    def __init__(self,iv=0,it=0,Max=None,Min=None):
        self._id=self.get_id()
        if max is not None:
            self.max=Max
        if min is not None:
            self.min=Min
        super().__init__(iv,it)
    def __setitem__(self, index, val):
        if index==0:
            if val>self.max or val<self.min:
                raise ValueError('{} is outside of allowed range,[{},{}] for state variable {}'.format(val,self.min,self.max,self._id))
            else:
                super().__setitem__(index,val)
        elif index==2:
            if val[0]>self.max or val[0]<self.min:
                raise ValueError('{} is outside of allowed range,[{},{}] for state variable {}'.format(val,self.min,self.max,self._id))
            else:
                super().__setitem__(index,val)
        else:
            super().__setitem__(index,val)
class UnitPool(type):
    """Manages conserved quantities
    If state variables are composed of conserved quantities, eg energy or mass, UnitPool
    """
    _units=0
    print("dat UnitPool metaclass dooeeee")
    @classmethod
    def __prepare__(cls, name, parents, **kwargs):
        print("__prepare__")
        return {}
    def __new__(cls, name, parents, dct):
        print("__new__")
        return super(UnitPool,cls).__new__(cls,name,parents,dct)
    def __init__(cls, name, parents, dct):
        cls.string="holder"
        print('__init__')
    def ReleaseUnits()
class conserved1(metaclass=UnitPool):
    pass
    
        
class Data(MutableMapping):
    def __init__(self,keys=['data'],data=None,*args,**kwargs):
        if data is None:
            try:
                self._storage={key: [] for key in keys}
            except:
                self._storage={keys: []}
        else:
            try:
                assert(all(isinstance(x,dict)for x in data))
                self._storage={}
                for key,item in zip(keys,data):
                    item.pop('name')
                    self._storage[key] = item
            except:
                try:
                    assert(all(isinstance(x,dict)for x in data))
                    self.storage={}
                    for item in data:
                        name = item.pop('name')
                        self._storage[name]=item
                except:
                    try:
                        self._storage={key: [dat] for key,dat in zip(keys,data)}
                    except:
                        try:
                            self._storage={key: dat for key,dat in zip(keys,data)}
                        except:
                            if len(data)!=len(keys):
                                print("data and key lists must be the same length")
                                raise ValueError
                    
                
    def __setitem__(self, key, val):
        try:
            self._storage[key]=val
        except:
            try:
                if type(val)==list:
                    self._storage[key]=val
                else:
                    self._storage[key]=[val]
            except:
                raise TypeError
        self._storage[key] = val
    def __getitem__(self, key):
        return self._storage[key]
    def __delitem__(self, key, index=None):
        if index is None:
            del self._storage[key]
        else:
            del self._storage[key][index]
    def __iter__(self):
        return iter(self._storage)
    def __len__(self):
        return len(self._storage)
    def __str__(self):
        '''returns simple dict representation of the mapping'''
        return str(self._storage)
    def __repr__(self):
        '''echoes class, id, & reproducible representation in the REPL'''
        return '{}, Data({})'.format(super(Data, self).__repr__(), 
                                  self._storage)
    def save(self,fn):
        df=pd.DataFrame(dict([(k,pd.Series(v)) for k,v in self._storage.items()]))
        print(df)
        df.to_json(fn)
class MarkovChain:
    def __init__(self):
        self.current_state=None
        self.possible_states=None
        self.Transitions=None

class KMC:
    def __init__(self,statevec):
        self.stop_criteria=False
        self.steps=0
        assert(type(statevec)==sv.StateVector)
                                               
    def reaction_propensities(self):
        pass
    def random_numbers(self):
        pass
    def generate_time_step(self):
        pass
    def determine_reaction(self):
        pass
    def update(self):
        pass
    def calculate_cumulative_function(self):
        pass
    def normalize_probability_function(self):
        pass
    def generate(self):
        pass
class Probability(metaclass=ABCMeta):
    def __init__(self, frequency):
        self.frequency=frequency
        self.probability_vector=None
    @abstractmethod
    def __call__(self,state,*args,**kwargs):
        pass
class Propensity(metaclass=ABCMeta):
    """Decorator to convert function "P(state variable) = probability of single state or transition" into "P(state vector) = vector of (probabilities, index). This is for linear propensities or propensities which are functions of only one state variable."
    
    use **kwargs for:
    indices = [list of indices] applies the function to given indices
    range = [start, end] or single integer applies function to indices in range(start,end) or range(single integer)
    index = single index: applies function to given index
    stoichiometry = for dat stoich
    use *args for:
    first argument will be the value of the state vector index

    example:
    import KMC
    @KMC.Propensity
    def harmonic(x,*args,**kwargs):
        if kwargs["length"] is None:
            kwargs["length"]=1
        return np.sin(x*args[0]*np.pi/kwargs["length"])
    x=sv.StateVector([1,1,1,1])
    print(harmonic(x,length=3,range=len(x.state)))
    # prints [(0.0, 0), (0.8660254037844386, 1), (0.8660254037844388, 2), (1.2246467991473532e-16, 3)]
    # note that index 3 is non-zero due to rounding error
    """
    def __init__(self,func,*args,**kwargs):
        self.propensity_function=func
        self.args=args
        self.kwargs=kwargs
        self.choice=None
    def __call__(self,state_vector,*args,**kwargs):
        self.state=state_vector
        print(kwargs)
        try:
            r_start=kwargs["range_start"]
            r_stop=len(self.state)
            if r_stop>r_start:
                return ((self.propensity_function(self.state[i],self.state[0],*args,**kwargs),i) for i in range(r_start,r_stop) if i>0)
            else:
                return 0.0
        except:
            try:
                rindices=kwargs["reactants"] # list of lists or tuples of reactant indices with repeats
                #pindices=kwargs["products"] # ditto for products

                return ((r,self.propensity_function(self.state[r],r,state=self.state,reactants=rindices)) for r in rindices)
            except:
                try:
                    reactant_range=kwargs["reactant_range"]
                    reaction_degree=kwargs["degree"]
                    react_sets=list(itt.combinations_with_replacement(range(reactant_range),reaction_degree))
                    return ((self.propensity_function([self.state[j] for j in i],i,frequency=kwargs["frequency"]),i) for i in react_sets)
                except:
                    try:
                        indices=kwargs["indices"]
                        return ((self.propensity_function(self.state[i],i,*args,**kwargs),i) for i in indices)
                    except:
                        try:
                            index=kwargs["index"]
                            return (self.propensity_function(self.state[index],index,*args,**kwargs),index)
                        except:
                            try:
                                index=kwargs["indices"]
                                return (self.propensity_function(self.state[index],index,*args,**kwargs),index)
                            except:
                                try:
                                    index_range=kwargs["range"]
                                    return ((self.propensity_function(self.state[i],i,*args,**kwargs),i) for i in range(index_range[0],index_range[1]))
                                except:
                                    try:
                                        return ((self.propensity_function(self.state[i],i,*args,**kwargs),i) for i in range(index_range))
                                    except:
                                        try:
                                            return ((self.propensity_function(self.state[0],*args,**kwargs),0))
                                        except:
                                            print("nothin")
                    
       
        
class InteractionProbability(Probability):
    def P_Pre(self,element,*args,**kwargs):
        return self.P(element,args,kwargs)
    @abstractmethod
    def P(self,element,*args,**kwargs):
        pass
    def __call__(self,state,*args,**kwargs):
        self.probability_vector=state.vectorize_non_zero(self.P_Pre,*args,**kwargs)
class IndexedProbability(Probability):
    def __init__(self, frequency):
        super().__init__(frequency)
        self.counter=0
    def __call__(self,state):
        self.counter=0
        self.probability_vector=state.vectorize_function(self.P_pre)
    def P_pre(self,element):
        self.counter+=1
        self.P(element)
    @abstractmethod
    def P(self,element):
        pass
class MonomerAddition(Probability):
    def __call__(self,state):
        self.probability_vector=state.vectorize_nonzero(self.Padd)
    def Padd(self,state,indices,*args,**kwargs):
        if indices[0]==0:
            indices=indices[1:]
            M=state[0]
        else:
            return [(0,0)]
        return [(M*state[i]*self.frequency,i) for i in indices]
class Nucleation(Probability):
    def __init__(self,nc,frequency):
        super().__init__(frequency)
        self.nc=copy.copy(nc)
        self.M_factor=1
    def __call__(self,state):
        M=state.sum(1)
        self.M_factor=1
        for i in range(copy.copy(self.nc)):
            self.M_factor*=M-i
        self.probability_vector=[(self.M_factor*self.frequency,0)]
class MonomerSubtraction(Probability):
    def __call__(self,state):
        self.probability_vector = state.vectorize_nonzero(self.Psub)
    def Psub(self,state,indices,*args,**kwargs):
        if indices[0]==0:
            indices=indices[1:]
        return [(2*self.frequency*state[i],i) for i in indices]
class Fragmentation(MonomerSubtraction):
    def __init__(self,nc,frequency):
        super().__init__(frequency)
        self.nc=nc
    def __call__(self,state):
        self.probability_vector = state.vectorize_nonzero(self.Pfrag)
        # if self.probability_vector is not None:
        #     self.probability_vector[1][0]=0
    def Pfrag(self,state,indices,*args,**kwargs):
        print(state,indices,"fraggin")
        if copy.copy(self.nc)>3:
            lim=copy.copy(self.nc)
        else: 
            lim=3
        [print("hur",i,state[i],(i-2)*state[i]*self.frequency) for i in indices if i>lim]
        out = [((i-2)*state[i]*self.frequency,i) for i in indices[1:] if i>lim]
        return out
class Coagulation(Probability):
    def __init__(self,frequency):
        super().__init__(frequency)
        self.counter=1
    def __call__(self,state):
        self.probability_vector = state.vectorize_nonzero(self.Pcoag)
    def Pcoag(self,state,indices,*args,**kwargs):
        #for i,v in enumerate(indices):
        print(indices,"indices")
        q=set(itt.chain(indices[1:],indices[1:]))
        w=list(itt.combinations(q,2))
        ww=[(i[0]*i[1]*self.frequency,i) for i in w]
        return ww

class Model:
    def __init__(self,state,nc):
        self.t_step=None
        self.nc=nc
        self.propensities=[]
        self.operations=[]
        self.frequencies=[]
        self.mechanisms=None
        self.state=state
        self.P=[]
        self.summed_P_vector=[]
        self.indices=[]
        self.data_list=['mass','number','polymers','skew','kurtosis','histogram','t_steps','t','state']
        self.data=Data(keys=self.data_list)
        # self.data={}
        # self.data["mass"]=[]
        # self.data["number"]=[]
        # self.data["polymers"]=[]
        # self.data["skew"]=[]
        # self.data["kurtosis"]=[]
        # self.data["histogram"]=[]
        # self.data["t_steps"]=[]
        # self.data["t"]=[]
        # self.data["state"]=[]
    # @property
    # def nc(self):
    #     return self.nc
    def add_propensity(self,propensity):
        self.propensities.append(propensity)
    def add_mechanisms(self,mechs):
        self.mechanisms=mechs
        print(self.mechanisms)
    def calculate_probability(self):
        self.P=[]
        self.summed_P_vector=[]
        for i in self.propensities:
            self.P.append(i(self.state.state))
        for i in self.P:
            try:
                self.summed_P_vector.append(sum(i))
            except:
                self.summed_P_vector.append(i)
        print(self.summed_P_vector)
        norm=sum(self.summed_P_vector)
        print(norm)
        self.norm_probability=[i/norm for i in self.summed_P_vector]
        print(self.norm_probability)
    def ready(self):
        self.P=[]
        self.indices=[]
        print(self.propensities)
        for ind,i in enumerate(self.propensities):
            print(i)
            self.P.append([])
            prop_func=i[0]
            ar=i[1]
            try:
                if ar["Range_stop"]==True:
                    ar["range_stop"]=len(self.state.state)
            except:
                try:
                    if ar["Range"]==True:
                        ar["range"]=len(self.state.state)
                except:
                    try:
                        if ar["Reactant_range"]==True:
                            ar["reactant_range"]=len(self.state.state)
                    except:
                        pass
            num=len(self.state.state)-1
            print("FUCK",len(self.state.state)-1)
            try:
                outp=list(prop_func(self.state.state,self.state[0],polymer_number=num,**ar))
            except:
                outp=prop_func(self.state,self.state[0],polymer_number=num,**ar)
            print(outp)
            print(ind)
            print(ind)
            print(ind)
            print(ind)
            print(ind)
            print(ind)
            print(ind)
            print(ind)
            self.P[ind].append(outp)
        print(self.P)
    def BulkProbability(self):
        self.bulk_P=[]
        for i in self.P:
            msum=0
            if type(i[0])==float or type(i[0])==int:
                self.bulk_P.append(i[0])
            else:
                for j in i:
                    try:
                        msum+=j[0]
                    except:
                        pass
                self.bulk_P.append(msum)
        sss=sum(self.bulk_P)
        self.norm_probability=[i/sss for i in self.bulk_P]

           
    def choose(self):
        self.choice=npr.choice(range(len(self.summed_P_vector)), p=self.norm_probability)
        print(self.choice)

    def time_step(self):
        self.t_step=(1/sum(self.summed_P_vector))*np.log10(1/npr.random())
        print(self.t_step,"Time Step")
    def saveData(self,fn):
        print(self.data)
        self.df=pd.DataFrame(self.data)
        self.df.to_pickle("results")
    def advance(self):
        print("CHOICE",self.choice)
        if self.choice==0:
            self.mechanisms.run("add")
            print("adding")
        if self.choice==1:
            print("subbing")
            self.mechanisms.run("subtract")
            # index=npr.choice(range(len(self.state.state[1:])))+1
            # self.state.state[index]=self.state.state[index]-1
            # if self.state.state[index]<self.nc:
            #     self.state.state[0]=self.state.state[0]+self.state.state[index]
            #     self.state.state[index]=self.state.state[index]-self.state.state[index]
            # self.state.state[0]=self.state.state[0]+1
        if self.choice==2:
            print("nucleating")
            self.mechanisms.run("nucleate")
            # print(self.state.state)
            # print(self.nc)
            # self.state.state.append(self.nc)
            # self.state.state[0]=self.state.state[0]-self.propensities[0].nc
        if self.choice==3:
            print("break")
            self.mechanisms.run("break")
            # print(self.state.state)
            # ss=sum([j for j in self.state.state if j>3])
            # print(ss,"ss")
            # pindex=npr.choice(range(ss))
            # print(pindex,"pindex")
            # i=0
            # count=0
            # while(i<pindex):
            #     count+=1
            #     if self.state.state[count]>3:
            #         i+=self.state.state[count]
            #     if i>pindex:
            #         r=i-pindex
            #         print(r,"r")
            #         print(count,"count")
            #         self.state.state[count]=self.state.state[count]-r
            #         if self.state.state[count]<self.nc:
            #             self.state.state[0]=self.state.state[0]+self.state.state[count]
            #             del self.state.state[count]
            #         if r<self.nc:
            #             self.state.state[0]=self.state.state[0]+r
            #         else:
            #             self.state.state.append(r)
        print("SUM",sum(self.state.state))
        if self.choice==4:
            print("merge")
            self.mechanisms.run("merge")
            # index=npr.choice(range(len(self.state.state[1:])))+1
            # r=self.state.state[index]
            # del self.state.state[index]
            # index=npr.choice(range(len(self.state.state[1:])))+1
            # self.state.state[index]=self.state.state[index]+r
        self.data["polymers"].append(np.sort(self.state.state[:]))          
        self.data["mass"].append(self.state.sum())
        self.data["number"].append(self.state.length())
        self.data["skew"].append(self.state.skew())
        self.data["kurtosis"].append(self.state.kurtosis())
        self.data["histogram"].append(self.state.histogram())
        self.data["t_steps"].append(self.t_step)
        self.data["t"].append(sum(self.data["t_steps"]))
        self.data["state"].append(copy.deepcopy(self.state))

if __name__ == '__main__':
    print("we in it")

