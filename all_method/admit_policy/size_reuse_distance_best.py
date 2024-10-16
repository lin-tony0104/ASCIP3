#取得hit_rate的MLP改成用統計的 region size 1000
#前100w筆
from .admit_BASE import admit_BASE
from lib.dequedict import DequeDict
from collections import defaultdict

#改寫DequeDict
class my_cache(DequeDict):
    '''
    保存cache內容
    使用region維護cache_value
    '''
    def __init__(self,cache_size):
        super().__init__()

        self.value=0#cache_value
        self.obj_num=0#cache中 obj數
    #
    def pushFirst(self, key, value):
        super().pushFirst(key, value)
        self.obj_num+=1
        self.value+=value.o_val       

    def _remove(self, key):
        value=super()._remove(key)
        self.obj_num-=1
        self.value-=value.o_val   
        

    def _push(self, key, value):
        super()._push(key, value)
        self.obj_num+=1
        self.value+=value.o_val   

 

    def get_avg_cache_value(self):
        if self.obj_num==0:
            return 0
        return self.value/self.obj_num

        
        

    

class SRDb(admit_BASE):
    class entry():
        def __init__(self,obj):
            self.o_size=obj.o_size
            self.o_block=obj.o_block
            self.o_ReuseDistance=0
            self.o_val=0
            self.hit=False

    def __init__(self,cache_size):
        self.req_num=0
        self.cache_size=cache_size
        self.cache=my_cache(cache_size)
        
        self.time=0
        self.prev_use_time=defaultdict(lambda: float('-inf'))#紀錄obj上次使用時間 初始0

#"""超參數調整方法: 先調整region_size 在調整alpha。"""
#"""原因 先看需要多少region才能有好效果   在調整alpha看多少必較符合trace的變動特性"""

        # self.region_size=1000
        # self.region=defaultdict(int)
        # self.alpha=0.2#  0:只看過往   1:只看現在



#wiki 超參數
        self.region_size=1000
        # self.region_size=100
        # self.region_size=10
        self.region=defaultdict(int)
        self.alpha=0.2#  0:只看過往   1:只看現在

# #twitter45 超參數
#         # self.region_size=1000         #46.79
#         self.region_size=1          
#         # self.region_size=10             #46.64
#         self.region=defaultdict(int)
#         self.alpha=0.2#  0:只看過往   1:只看現在
# #twitter24 超參數
#         # self.region_size=1000         #
#         self.region_size=1          
#         # self.region_size=10             #
#         self.region=defaultdict(int)
#         self.alpha=0.2#  0:只看過往   1:只看現在


# #twitter29 超參數
#         # self.region_size=5000     #76.38
#         self.region_size=2000     #76.44
#         # self.region_size=1000     #76.42
#         # self.region_size=500        #76.36
#         # self.region_size=100        #76.15
#         # self.region_size=10       #76.11
#         self.region=defaultdict(int)
#         # self.alpha=0.01#  0:只看過往   1:只看現在 76.52
#         self.alpha=0.05#  0:只看過往   1:只看現在 76.52
#         # self.alpha=0.1#  0:只看過往   1:只看現在 76.51
#         # self.alpha=0.2#  0:只看過往   1:只看現在 76.44
#         # self.alpha=0.5#  0:只看過往   1:只看現在 76.18
#         # self.alpha=0.9#  0:只看過往   1:只看現在 75.54

        

# #mix_wiki_29 超參數
#         # self.region_size=50000   #68.07
#         # self.region_size=10000   #68.05
#         self.region_size=5000   #68.02
#         # self.region_size=2000   #67.98
#         # self.region_size=1000   #67.94
#         # self.region_size=100      #67.93
#         # self.region_size=10     #67.92
#         self.region=defaultdict(int)
#         # self.alpha=0.05#  0:只看過往   1:只看現在 68.03
#         self.alpha=0.1#  0:只看過往   1:只看現在 68.03
#         # self.alpha=0.2#  0:只看過往   1:只看現在 68.02
#         # self.alpha=0.5#  0:只看過往   1:只看現在 68.0
#         # self.alpha=0.9#  0:只看過往   1:只看現在 67.77

    def request(self, obj):
        self.time+=obj.o_size
        r=obj.o_size//self.region_size
        self.req_num+=1

        self.curr_obj=self.entry(obj)
        self.curr_obj.o_ReuseDistance=self.time-self.prev_use_time[obj.o_block]  #可改成 prev_use_time[obj.o_block]
        self.prev_use_time[obj.o_block]=self.time

        self.curr_obj.o_val=max(self.cache_size-self.curr_obj.o_ReuseDistance,0)/self.curr_obj.o_size
        # print(self.curr_obj.o_val)
        self.region[r]=(1-self.alpha)*self.region[r] + self.alpha*self.curr_obj.o_val
        



    def evict(self, victim):
        del self.cache[victim.o_block]


        

    def hit(self, obj):
        self.cache[obj.o_block]=self.curr_obj
        self.cache[obj.o_block].hit=True
        
    def addToCache(self, obj):
        self.cache[obj.o_block]=self.curr_obj


    def GET_DEBUG_MESSAGE(self):
        message="cache_value:"+str(self.cache.get_avg_cache_value())\
        +"  alpha: "+str(self.alpha)\
        +"  region_size: "+str(self.region_size)
        return message    

    def judge(self,obj):
        #有剩餘空間直接准入
        r=obj.o_size//self.region_size
        # if self.req_num<10000000:#warmup
        #     return True
        if self.curr_obj.o_size<(self.cache_size-self.cache.cached_count):
            return True
        else:
            # print(obj.o_val)
            # if self.curr_obj.o_val>self.cache.get_avg_cache_value():
            if self.region[r]>self.cache.get_avg_cache_value():
                return True
            else:
                return False