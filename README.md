# 我的ASC-Admission

這個程式有下列部分:
- run.py: 負責程式執行介面(ex:選擇evict_policy,選擇admit_policy,設定cache_size,選trace_file)
- cache_system.py: 完整的cache執行流程，呼叫evict_policy,admit_policy
- evict_policy(資料夾):所有驅逐策略
- admit_policy(資料夾):所有准入策略(主要:ASC_Admission.py)
