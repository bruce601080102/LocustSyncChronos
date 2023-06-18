## LocustSyncChronos
---
<a href="/atiksoftware/pubg_mobile_memory_hacking_examples/blob/LocustSyncChronos">
<img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/eagle705/brucesplit" alt="Hits" data-canonical-src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/eagle705/LocustSyncChronos" style="max-width:100%;"></a> 

![DEMO](./images/demo.png)
## 專案介紹
這個項目旨在改善Locust在分散式連線方面的限制，並提供一個使用者友好的管理介面。它還具備計時器功能，以便在進行壓力測試時能夠控制和監視執行時間。此外，該介面還支持將腳本同步到不同的worker上，以便在分散式部署中保持腳本的一致性。

##  主要功能
* 分散式連線管理：通過管理介面，用戶可以指定目標URL和連線數量，以及設定連線的生成速率。系統將自動分發連線到不同的worker上，實現分散式的壓力測試。

* 時間計時器：管理介面具備計時器功能，用戶可以設定執行時間，控制壓力測試的持續時間。計時器可以顯示剩餘時間並提供結束測試的選項。

* 腳本同步：用戶可以通過管理介面將測試腳本同步到不同的worker上。這確保了在分散式部署中，所有的worker都運行相同的腳本，測試結果的一致性。

## 專案特色

- [x] 單點壓測
- [x] 分散式壓測
- [x] 自動化壓測
- [x] 計時停止壓測
- [x] 自動化生成csv
- [x] 管理介面

## 用法
1. **下載專案**
    ```sh
    git clone https://github.com/bruce601080102/LocustSyncChronos.git
    ```

2. **安裝包**
    ```sh
    pip install -r requirements.txt
    ```
    [詳細使用說明](Github專案部署)


## 筆記
[locust使用筆記](https://www.notion.so/locust-16c0926f26f54565a393f02204564653)




