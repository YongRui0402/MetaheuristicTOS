# 啟發演算發演算法轉珠遊戲最佳路徑搜尋研究
轉珠遊戲是一個數學的益智遊戲，讓玩家透果轉動版面中的珠子，使版面可以消除盡可能多的珠子來獲得高分。本實驗比較了三種演算法，Iterative Deepening Depth-First Search (IDFS)、Genetic Algorithm(GA)與Ant Colony Optimization(ACO)，來嘗試解決轉珠最佳路徑的搜尋問題，實驗結果發現在計算資源小於２秒與最大路徑長為25的情況下GA所獲得的分數均由於IDFS與ACO。


## Python 依賴
這個專案依賴於以下Python的函式庫：
1. NumPy
2. random
3. timeit
* 您可以使用以下命令安裝這些依賴：
    ```bash 
    pip install numpy
    # random與timeit為內建
    ```
## 實驗
### 這個專案進行了以下幾種實驗：

* Exp1: 參數優化
這個實驗的目的是優化演算法的參數。詳細的實驗程式可以在/source_code/實驗/中找到Exp1.py。

* Exp2: 演算法效能比較（1206組版面評估）
這個實驗對不同的演算法進行了效能比較，包括在1206組版面評估中的效能。詳細的實驗程式可以在/source_code/實驗/中找到Exp2.py。

* Exp3: 不同最大路徑演算法效能比較（35, 45）
這個實驗對於不同最大路徑的演算法效能進行了比較，包括在35和45這兩種情況下的效能。詳細的實驗程式可以在/source_code/實驗/中找到Exp3.py。

* Exp4: 不同計算資源演算法效能比較（2s, 3s）
這個實驗對於不同計算資源（在2秒和3秒內）的演算法效能進行了比較。詳細的實驗程式可以在/source_code/實驗/中找到Exp4_2s.py,Exp4_3s.py。

* 如何運行
請在此說明如何運行您的程式。
``` python = 1
python Exp1.py  # 運行 Exp1 程式碼
python Exp2.py  # 運行 Exp2 程式碼
python Exp3.py  # 運行 Exp3 程式碼
python Exp4_2s.py  # 運行 Exp4 程式碼
python Exp4_3s.py  # 運行 Exp4 程式碼
```

# 具體專案內容與實驗結果請參照 
* 超啟發演算法專題報告.pdf
* experimental_data/實驗結果整理.xlsx

## 目前程式問題與修改方向
* 20240415
    * 檔案分類架構混亂
    * 演算法尚可優化