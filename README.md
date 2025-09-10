# Hadoop 3-node cluster (Docker/Codespaces)

This repo runs a minimal Hadoop cluster (1 master, 2 workers) in 3 Docker containers.

## Quick start

You can run this locally with Docker Desktop or inside GitHub Codespaces.

1) Start the cluster

```bash
docker compose up -d --build
```

2) UIs (forwarded ports)

- NameNode: 9870
- YARN ResourceManager: 8088
- MapReduce History: 19888

## Run WordCount

```bash
docker exec -it hadoop-master bash -lc '
hdfs dfs -mkdir -p /input &&
echo "to be or not to be" > /tmp/text.txt &&
hdfs dfs -put -f /tmp/text.txt /input &&
hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /input /output &&
hdfs dfs -cat /output/part-r-00000
'
```

Expected output includes lines like:

```
be      2
to      2
not     1
or      1
```

Source du job WordCount (Java):

- https://github.com/apache/hadoop/blob/1be78238728da9266a4f88195058f08fd012bf9c/hadoop-mapreduce-project/hadoop-mapreduce-examples/src/main/java/org/apache/hadoop/examples/WordCount.java

## Optional: verify HDFS

```bash
docker exec -it hadoop-master bash -lc 'hdfs dfsadmin -report'
```

You should see “Live datanodes (2)”.

### See the HDFS filesystem (tree)

```bash
docker exec -it hadoop-master bash -lc 'hdfs dfs -ls -R /'
```

## Troubleshooting

- NameNode safe mode: if you see “Cannot create file … Name node is in safe mode.”

   ```bash
   docker exec -it hadoop-master bash -lc 'hdfs dfsadmin -safemode leave'
   ```

- UIs not reachable: ensure the containers are up and the ports aren’t occupied. Recreate the stack:

   ```bash
   docker compose down -v && docker compose up -d --build
   ```

## Stop cluster

```bash
docker compose down -v
```
