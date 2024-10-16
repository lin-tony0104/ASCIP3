'''
run.py完成下列項目:
1. CMD介面+功能
2. 選擇演算法
'''


from cache_system import cache
import matplotlib.pyplot as plt

#evict_policy
from evict_policy.FIFO import FIFO
from evict_policy.lru import LRU
from evict_policy.lfu import LFU
from evict_policy.lecar import LeCaR
from evict_policy.Belady_size import Belady_size
from evict_policy.GDS import GDS
#admit_policy
from admit_policy.all_admit import ALL_ADMIT
from admit_policy.ASC_Admission import ASC_Admission
from admit_policy.size_reuse_distance_v2 import SRDb_v2
from admit_policy.size_reuse_distance_v3 import SRDb_v3
from admit_policy.size_reuse_distance_v4 import SRDb_v4
from admit_policy.size_reuse_distance_v5 import SRDb_v5
from admit_policy.size_reuse_distance_v6 import SRDb_v6
from admit_policy.size_reuse_distance_v7 import SRDb_v7
from admit_policy.size_reuse_distance_v8 import SRDb_v8
from admit_policy.size_reuse_distance_v10 import SRDb_v10
from admit_policy.size_reuse_distance_v11 import SRDb_v11
from admit_policy.size_reuse_distance_v12 import SRDb_v12
from admit_policy.size_reuse_distance_best import SRDb

class my_list:
    def __init__(self,name,options):
        self.name=name
        self.options=options
    
    def choice(self):
        info=self.name+":"
        for i in range(len(self.options)):
            info+= (" "+str(i)+"."+self.options[i])

        c=int(input(info))
        return self.options[c][1]





def get_unit(e,a,t):
    default_cache_size=0

    name_list=["evict_policy","admit_policy","trace_file"]
    unit_list=[e,a,t]

    result=[]
    selected_info=[]
    for  name , unit in zip(name_list,unit_list):
        info="\nselect the "+name+":\n"
        
        for i in range(len(unit)):
            info+=str(i)+"."+ unit[i][0]+"   "
        info+="\nenter: "
        i=int(input(info))
        selected=unit[i][1]
        selected_info.append(unit[i][0])
        result.append(selected)

        if name=="trace_file":
            default_cache_size=unit[i][2]

    evict_policy=result[0]
    admit_policy=result[1]
    trace_file=result[2]


    cache_size=int(input("cache_size:"))    
    if cache_size==0: cache_size=default_cache_size
    print("cache_size: ",cache_size)


    return cache_size , evict_policy , admit_policy , trace_file ,selected_info

if __name__ == '__main__':
    print('==============================================================')
    hits = 0
    requests = 0

    #如果有心的策略,trace 要更新下面三個
    evict_list=[("LRU",LRU),("LFU",LFU),("LeCaR",LeCaR),("FIFO",FIFO),("Belady_size",Belady_size),("GDS",GDS)]
    admit_list=[("all_admit",ALL_ADMIT),("ASC_Admission",ASC_Admission),("size_reuse_distance_best",SRDb),("size_reuse_distance_v2",SRDb_v2),("size_reuse_distance_v3",SRDb_v3),("size_reuse_distance_v4",SRDb_v4),("size_reuse_distance_v5",SRDb_v5),("size_reuse_distance_v6",SRDb_v6),("size_reuse_distance_v7",SRDb_v7),("size_reuse_distance_v8",SRDb_v8),("size_reuse_distance_v10",SRDb_v10),("size_reuse_distance_v11",SRDb_v11),("size_reuse_distance_v12",SRDb_v12)]
    trace_list=[("wiki_10","D:/all_Trace/ASC-IP/wiki_10",241892558105),("wiki2018_reuse","D:/all_Trace/ASC-IP/wiki2018_reuse",21990232555),("wiki2018.tr","D:/all_Trace/ASC-IP/wiki2018",21990232555),("twitter29","D:/all_Trace/ASC-IP/Twitter29",109951162),("MIX_wiki_29","D:/all_Trace/ASC-IP/MIX_wiki_29",21990232555),("Twitter45","D:/all_Trace/ASC-IP/Twitter45",10737418),("MIX_wiki_45","D:/all_Trace/ASC-IP/MIX_wiki_45",2748779069),("twitter24","D:/all_Trace/ASC-IP/Twitter24",27487790),("MIX_wiki_24","D:/all_Trace/ASC-IP/MIX_wiki_24",21990232555)]# default_cache_size: 20% working_set_size*0.005  (ascip論文搜尋:X)


   
    cache_size , evict_policy , admit_policy , trace_file , selected_info = get_unit(evict_list,admit_list,trace_list)
    #例外狀況
    if cache_size <= 0:
        print("Cache_size should be greater than 0")
        exit(1)
    
    #init
    evict=evict_policy(cache_size)
    admit=admit_policy(cache_size)

    #組裝 admit,evict
    alg = cache(admit,evict,cache_size)
    alg.DEBUG_CACHE_INFO=selected_info[0] +" / "+ selected_info[1] +" / "+ str(cache_size)
    
    #-----------------------------------------




    with open(trace_file, 'r') as f:
        for line in f:
            temp=line.split()

            lba = int(temp[0])
            size = int(temp[1])

            #如果沒有reuse資訊的話就是-1
            reuse=-1
            if len(temp)>2:
                reuse=int(temp[2])

            if size>cache_size:#如果不寫會造成矛盾， 請求到的object一定會放入cache，但同時又放不下。
                print("object size greater then cache size. SIZE:",size)
                exit(1)

            if lba < 0:
                continue
            requests += 1

            hit = alg.requests(lba,size,reuse)

            if hit:
                hits += 1
            
            misses = requests - hits
            


                    # self.evict_policy.DEBUG_show_para()
            if not alg.DEBUG_requests%1000000:
                trace_file_name=trace_file.split("/")[-1]
                result=trace_file_name+" "+alg.DEBUG_show_useTime()
                print(result)



