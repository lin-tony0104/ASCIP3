#老師說的
from lib.dequedict import DequeDict
# from ..lib.heapdict import HeapDict
import numpy as np
from .admit_BASE import admit_BASE
 



class ASC_Admission(admit_BASE):
    class ASC_Admission_entry:
        def __init__(self,obj,admitted=False,hit=False):
            self.o_block=obj.o_block
            self.o_size=obj.o_size
            self.admitted=admitted
            self.hit=hit
            
            self.main_cache_entry=obj
            
    def __init__(self,cache_size):
# wiki
        self.delta=200 #超參數
        self.c=20000

        # self.c=6000
        # #第一次cache滿的 hit_rate
        # self.delta=50 #84.42
        # self.delta=10 #83.45
        # self.delta=50 #82.11
        # self.delta=100 #81.2
        # self.delta=200 #81.19
        # self.delta=500  #80.07
        # self.delta=1000  #78.72
        # self.delta=3000  #78.61


        self.cache_size=cache_size
        self.cache=DequeDict()
        self.history=DequeDict()
        np.random.seed(0)

        


    # def request(self,obj):
    #     x=self.cache[obj.o_block] if obj.hit else self.ASC_IP_entry(obj,admitted=False,hit=obj.hit)

    def hit(self,obj):
        self.cache[obj.o_block].hit=True

    def evict(self,victim):
        x=self.cache[victim.o_block]
        del self.cache[victim.o_block]
        self.adjust_C(x)
        self.addToHistory(x)

    def not_admit(self,obj):
        x=self.ASC_Admission_entry(obj)
        self.adjust_C(x)
        self.addToHistory(x)
    
    def addToCache(self,obj):
        x=self.ASC_Admission_entry(obj,admitted=True,hit=False)
        self.cache[obj.o_block]=x
    

    def judge(self,obj):#判斷是否admit
        p=np.exp(-obj.o_size/self.c)
        r=np.random.rand()
        if obj.o_size>self.c and p<=r:
            return False
        else:
            return True
    def GET_DEBUG_MESSAGE(self):
        message="  ||||||  c:"+str(self.c)\
        +"  admit_cache_count:"+str(self.cache.cached_count)\
        +"  c_delta:"+str(self.delta)
    
        return message 
#====================================================

    def adjust_C(self,obj):
        if obj.admitted and obj.hit==False:
            self.c-=self.delta
        elif not obj.admitted and obj.o_block in self.history:
            self.c+=self.delta
        if self.c<=0:
            self.c=1
    def addToHistory(self,obj):
        #清空間
        if (obj.o_block in self.history):
            del self.history[obj.o_block]
        else:
            while(self.cache_size-self.history.cached_count<obj.o_size):
                victim=self.history.popFirst()
        #放進去
        self.history[obj.o_block]=obj