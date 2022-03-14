# readFile
读文件，并将文件原样输出
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
PYSPARK_PYTHON=/home/ochadoop/apps/Python3/bin/python3 spark-submit \
--master yarn \
--deploy-mode cluster \
--conf spark.yarn.executor.memoryOverhead=4096 \
--num-executors 80 \
--executor-cores 5 \
--executor-memory 20G \
--driver-memory 12G \
--archives hdfs:///duizhang/Python3.zip#ANACONDA \
--conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=/home/ochadoop/apps/Python3/bin/python3 \
--files /home/ochadoop/apps/spark/conf/hive-site.xml \
spark2hive_sprd222.py
```
