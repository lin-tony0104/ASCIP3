#已完成
from lib.heapdict import HeapDict
from .evict_BASE import evict_BASE
class GDS(evict_BASE):
    class Entry:
        def __init__(self,obj,L,C):
            self.o_block=obj.o_block
            self.o_size=obj.o_size
            self.H=L+(C/obj.o_size)

            self.main_cache_entry=obj#為了回傳cache_entry，所以保存



        def __lt__(self,other):
            if self.H==other.H:
                return self.o_block<other.o_block
            return self.H<other.H
        

    def __init__(self,cache_size):
        self.cache_size=cache_size
        self.cache=HeapDict()
        self.L=0
        self.C=1   #論文中的cost (其他狀況下cost用來表示:download letancy,network cost等等 若無則設1)

        self.recent_hit=0
    

#============================    
    def request(self,obj):
        '''接收「request資訊」 , req_obj型態是cache_Entry'''
        if obj.hit:
            self.recent_hit+=1
            self.cache[obj.o_block]=self.Entry(obj,self.L,self.C)

    def addToCache(self,obj):
        #剛清完空間，把obj放入cache
        """接收「新增到cache的obj」 , obj型態是cache_Entry"""
        obj=self.Entry(obj,self.L,self.C)
        self.cache[obj.o_block]=obj
         
    def evict(self):
        victim=self.cache.popMin()
        self.L=victim.H
        return victim.main_cache_entry #



    def GET_DEBUG_MESSAGE(self):
        recent_hit_rate=round(100*self.recent_hit/1000000,2)
        result=" region_hit_rate: "+str(recent_hit_rate)
        self.recent_hit=0

        return result