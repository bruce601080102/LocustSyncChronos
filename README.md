<div align="center">
    <a href="image/about_icon05.png">
        <img src="https://miro.medium.com/max/1000/1*iHbPgMP5K4WWaP2RDBD37w.png" alt="Logo" width="80" height="80">
    </a>
    <h3 align="center">Locust 自動化壓測系統</h3>
</div>

## 專案特色

- [x] 單點壓測
- [x] 分散式壓測
- [x] 自動化壓測
- [x] 計時停止壓測
- [x] 自動化生成csv

## 當前版本(v2.0.0)
- 修正rps抓不對的問題
- 無須執行shell sript，只需執行python main.py即可

## 文件
* [Drawio -壓測系統流程圖](https://app.diagrams.net/#G16ziCpYF0JZqqCHCFr2mBbwDy79TjjtS5)

## 用法
1. **下載專案**
    ```sh
    git clone https://gitlab.hitrustai.com/bruce60108010204/stress-test.git
    ```

2. **安裝包**
    ```sh
    apt-get update
    apt-get upgrade -y
    apt-get install -y python3-opencv
    pip install -r requirements.txt
    ```

3. **指令控制部屬(單點)**
    * `單點master與worker`
        ```sh
        cd locust_scheduler
        vim buidMaster.sh
        python main.py -m shell
        ```
    * `多點master與worker`
        ```sh
        cd locust_scheduler
        ```
        - 先啟動worker
            ```sh
            python main.py -m worker -i 127.0.0.1 -p 5558
            ```
        - 再啟動master
            ```sh
            python main.py -m master -f flask_test.py
            ```
        > 注意:一定要先啟動worker

4. **GUI畫面控制部屬(單點/多點)**
    *  `壓測環境(可以控制docker的母體環境)`
        ```sh
        cd server
        python Server.py  
        ```
    *  `壓測環境(可以控制docker的母體環境)`
        ```sh
        cd server
        python Server.py  
        ```
    * `master`
        ```sh
        python main.py -m master -f flask_test.py
        ```

    * `多臺slave`
        <!-- ```sh
        locust -f locust_test.py --worker --master-host=192.168.10.101 --master-port=5558
        ``` -->
        ```sh
        python main.py -m worker -i 127.0.0.1 -p 5558
        ```
5. **程式執行**
    *  `在Master環境裡`
    *  `conf/env.conf 設定`
        ```sh
        [LoadTest]
        number_users = 100  (使用者數量)
        rate = 100 (上升數量)
        local_host = http://localhost:8089 
            (本地IP 最後不要有'/',單點port:8089，多點port:8090)
        target_host = http://192.168.10.111 (壓測IP 最後不要有'/')
        time_sec = 5 (壓測時間(秒數))

        [OutputFile]
        title = test2 (壓測主題)
        savepath = output/test.csv (做完一全部的壓測，請將此檔案刪除)
        container_name = diia(容器名稱)

        [GRPCDockerSet]
        cpu_count = 16,8,4,2 (需要測試的CPU核心數)
        total_ram_gb = 8 (需要測試RAM大小(GB))
        
        [Driver]
        is_open_headless = yes (是否打開無頭模式 yes/no)
        time_wait = 10 (更換容器配置後需幾秒後啟動壓測)
        ```
    *  `創建output`
        ```sh
        mkdir output
        ```    

    *  `執行`
        ```sh
        將buidMaster.sh裡的註解給解除(每次只能弄一組)
        ```
        ```sh
        python main.py
        ```
5. **檔案**
    * 報告取得位置: http://localhost:8090/stats/report
    *  `程式執行完，在output資料夾中將產生test.csv檔案`

## 注意
1. **更換docker 核心數與RAM**
    * 每次更改後，不用重啟程式，請改conf/env.conf中cpu_count的數值，改完即會動執行。
2. **修改locust_test.py**
    * 程式全部重啟，包括`locust及main.py`。
3. **分散式** 
    * 一旦master的locust終止程式，其他slave環境將會自動被斷開，需手動重啟。

## 測試
cd stress-test/test/flask_test
```sh
export DISPLAY=:1
```

```sh
flask run --debugger --no-reload --host 0.0.0.0 --port 9999
 * Debug mode: off
```

```sh
python main.py
```

## 線上筆記
https://www.notion.so/locust-16c0926f26f54565a393f02204564653