'''
v5 將v3的region 初始值改成平均reuse_distance*size   #這樣一來 rd大部分時候會是對的
v6: 
    1.由於v5可能出現cache類似LFU囤積的現象，   即cache_cost達到某個夠小的數值之後 ，熱門的obj大於該數值 持續造成miss
    2.將debug新增一項   近100w次的hit_rate 方便及早觀察是否收斂了

'''
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

        self.cost=0#cache_value
        self.obj_num=0#cache中 obj數
    #
    def pushFirst(self, key, value):
        super().pushFirst(key, value)
        self.obj_num+=1
        self.cost+=value.o_cost      

    def _remove(self, key):
        value=super()._remove(key)
        self.obj_num-=1
        self.cost-=value.o_cost  
        

    def _push(self, key, value):
        super()._push(key, value)
        self.obj_num+=1
        self.cost+=value.o_cost  

 

    def get_avg_cache_cost(self):
        if self.obj_num==0:
            return 0
        return self.cost/self.obj_num



        

    

class SRDb_v6(admit_BASE):
    class entry():
        def __init__(self,obj,time):
            self.o_size=obj.o_size
            self.o_block=obj.o_block
            self.o_cost=0
            self.o_time=time    #req的時間
            self.hit=False

    def __init__(self,cache_size):
        self.req_num=0
        self.cache_size=cache_size
        self.cache=my_cache(cache_size)
        self.history=DequeDict()
        
        self.time=0
        self.avg_reuse_distance=0
        self.recent_hit=0

#wiki超參數
        # self.region_size=1                  #59.17 
        # self.region_size=200            #  59.18
        # self.region_size=1500            #59.18  ok
        # self.region_size=700            #59.18
        self.region_size=1000           #59.17
        self.region=defaultdict(int)
        # self.alpha=0.08#  0:只看過往   1:只看現在
        self.alpha=0.9#  0:只看過往   1:只看現在
        # self.alpha=0.2#  0:只看過往   1:只看現在

#tw        



    def request(self, obj):
        self.time+=obj.o_size
        r=obj.o_size//self.region_size
        self.req_num+=1

        self.curr_obj=self.entry(obj,self.time)
        curr_reuse_distance=0
        #shadow_LRU 用來計算reuse_distance。   只要req到 就會放入該history
        if obj.o_block in self.history:
            curr_reuse_distance=self.time-self.history[obj.o_block].o_time #reuse_distance可能大於cache_size    因為obj在history裡的這段期間內 有其他req重用時並不會把 obj往前推。
            self.curr_obj.o_cost=curr_reuse_distance*self.curr_obj.o_size 
        else:
            curr_reuse_distance=self.cache_size
            self.curr_obj.o_cost=curr_reuse_distance*self.curr_obj.o_size   #rd設為 cache_size(較大的值)
            while(self.history.cached_count+obj.o_size>(self.cache_size)):
                self.history.popFirst()
        # print(self.curr_obj.o_val)


        self.history[obj.o_block]=self.curr_obj

        self.avg_reuse_distance=(1-self.alpha)*self.avg_reuse_distance+self.alpha*curr_reuse_distance #更新avg_reuse_distance
        if self.region[r]==0: #設定region[r]的初始值
            self.region[r]=self.avg_reuse_distance*obj.o_size


        
        self.region[r]=(1-self.alpha)*self.region[r] + self.alpha*self.curr_obj.o_cost
        



    def evict(self, victim):

        del self.cache[victim.o_block]


        

    def hit(self, obj):
        self.cache[obj.o_block]=self.curr_obj
        self.cache[obj.o_block].hit=True
        self.recent_hit+=1
        
    def addToCache(self, obj):
        self.cache[obj.o_block]=self.curr_obj


    def GET_DEBUG_MESSAGE(self):
        recent_hit_rate=round(100*self.recent_hit/1000000,2)
        message="cache_cost:"+str(self.cache.get_avg_cache_cost())\
        +"  alpha: "+str(self.alpha)\
        +"  region_size: "+str(self.region_size)\
        +"  avg_reuse_distance: "+str(self.avg_reuse_distance)\
        +"  recent_hit_rate:"+str(recent_hit_rate)

        self.recent_hit=0

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
            if self.region[r]<self.cache.get_avg_cache_cost():
                return True
            else:
                return False
            
