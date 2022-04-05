# ansibleforpy.py
ansilbe的官方案例

# ansforpy.py
按指定格式输出
节点IP       进程ID   CPU 使用率       使用内存       状态        运行时间

运行时注意点：
- 1.具体检索的进程在ansible运行的命令行中
- 2.需要配置hosts文件，并在py脚本中指定



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
输出文件到本地，或hdfs
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
输出文件到hdfs上
```
PYSPARK_PYTHON=/home/hadoop/apps/Python3/bin/python3 spark-submit \
--master yarn \
--deploy-mode cluster \
--conf spark.yarn.executor.memoryOverhead=4096 \
--num-executors 80 \
--executor-cores 5 \
--executor-memory 20G \
--driver-memory 12G \
--archives hdfs:///duizhang/Python3.zip#ANACONDA \  #这个zip是打包的python3的环境，里面最重要的是程序调用的公开包
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/home/hadoop/apps/Python3/bin/python3 \
--files /home/hadoop/apps/spark/conf/hive-site.xml \
spark2hive_sprd222.py
```
