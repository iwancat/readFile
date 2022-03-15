# readFile
目前版本是读文件，并将文件原样输出，中间数据因不需要处理所以没做变更，实现功能：
- 1.历史文件处理后直接改名，当日文件不改名
- 2.跨天时间段文件处理后改名
- 3.文件名查重
- 4.支持断点重处理
- 5.临时目录机制，支持竞争获取




# 连接pyhive
连接pyhive的方式
# 通过pyspark连接spark
python连接spark的方式
### client模式
```
spark-submit \
--master yarn \
--deploy-mode client \
--conf spark.yarn.executor.memoryOverhead=4096 \
--executor-memory 12G \
--num-executors 6 \
--executor-cores 8 \
--driver-memory 4G \
--files /home/ochadoop/apps/spark/conf/hive-site.xml \
spark2hive_sprd.py
```

### cluster模式
```
PYSPARK_PYTHON=/home/hadoop/apps/Python3/bin/python3 spark-submit \
--master yarn \
--deploy-mode cluster \
--conf spark.yarn.executor.memoryOverhead=4096 \
--num-executors 80 \
--executor-cores 5 \
--executor-memory 20G \
--driver-memory 12G \
--archives hdfs:///duizhang/Python3.zip#ANACONDA \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/home/hadoop/apps/Python3/bin/python3 \
--files /home/hadoop/apps/spark/conf/hive-site.xml \
spark2hive_sprd222.py
```
