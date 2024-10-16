#已完成
from lib.heapdict import HeapDict
from .evict_BASE import evict_BASE


class Belady_size(evict_BASE):
    class Entry:
        def __init__(self,obj):
            self.o_block=obj.o_block
            self.o_size=obj.o_size
            self.o_cost=obj.o_size*obj.o_reuse
            
            self.main_cache_entry=obj#為了回傳cache_entry，所以保存

        def __lt__(self,other):
            #min_heap
            if self.o_cost<0 or other.o_cost<0: #當reuse_distance=-1時 表示cost無限大，是特殊狀況 額外做處理
                #(other.o_cost<0):對方cost無限大   不論我是不是無限大都沒必要繼續heapupify (即:return False)
                #能進if 對方卻不是無限大 說明self是無限大 繼續hepupify (即:return True)
                return not other.o_cost<0 

            return (-self.o_cost) < (-other.o_cost) #取負數是為了讓它pop_min可以踢掉cost最大者
            
            #return true:會繼續heapupify
            #return false:會停止
    def __init__(self,cache_size):
        self.cache_size=cache_size
        self.cache=HeapDict()
        self.recent_hit=0
    

#============================    
    def request(self,obj):
        '''接收「request資訊」 , req_obj型態是cache_Entry'''
        if obj.hit:
            self.recent_hit+=1
            self.cache[obj.o_block]=self.Entry(obj)


    def addToCache(self,obj):
        #剛清完空間，把obj放入cache
        """接收「新增到cache的obj」 , obj型態是cache_Entry"""
        obj=self.Entry(obj)
        self.cache[obj.o_block]=obj
    def GET_DEBUG_MESSAGE(self):

        recent_hit_rate=round(100*self.recent_hit/1000000,2)
        result=" region_hit_rate: "+str(recent_hit_rate)
        self.recent_hit=0

        return result
    def evict(self):
        return self.cache.popMin().main_cache_entry #

