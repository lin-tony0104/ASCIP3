# 我的ASC-Admission

這個程式有下列部分:
- run.py: 負責程式執行介面(ex:選擇evict_policy,選擇admit_policy,設定cache_size,選trace_file)
- cache_system.py: 完整的cache執行流程，呼叫evict_policy,admit_policy
- evict_policy(資料夾):所有驅逐策略
- admit_policy(資料夾):所有准入策略(主要:ASC_Admission.py)



# TRACE
trace下載網址:https://drive.google.com/file/d/17lv8Zd6DG1TyBdJw1WlGV25heeicDuYp/view?usp=sharing

trace位置 "D:/all_Trace/ASC-IP/wiki2018"

trace格式 : 每一行是一個request，且每行內容為 id , size

註:原始格式為 : 每一行是一個request，且每行內容為 time , id , size , extra_feature
原始版本網址 : https://github.com/sunnyszy/lrb
