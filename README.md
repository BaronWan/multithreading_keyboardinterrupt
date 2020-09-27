### How to effectively solve the keyboard interruption by multi-threading and notify all sub-threads in time to handle the correct end of the program ?

> 多執行緒如何有效解決當鍵盤中斷時，能適時通知所有的子線程，以處理正確的結束程序 ?
> 
> Python 最好玩的地方就是，它其實提供了許多解決辦法來處理你的問題及你想要的結果。前提是，整合各知識並善用他們，是 python coder 必須要搞定的事情。

#### threading_kbint_sample.py
> 基本詮釋一解決方案

#### threading_kbint_sample_class.py
1. 採用 class 做正式的規劃設計
2. 運用 threading 的 Event.wait() 事件觸發來提昇事件的響應速度
3. 更完善的監督確認所有子線程的結束, 友善的結束程序。

#### threading_ctypes_raise_sample.py
1. 採用 ctypes api 進行觸發子線程的例外事件 (raise exception), 讓所有子線程立即結束動作後返回。
2. 整體設計使得 外部的子線程建議程序 能加入運行。
