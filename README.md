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

## Run WordCount in Python (Hadoop Streaming)

Example mapper/reducer are in `examples/python/wordcount/`.

```bash
docker exec -it hadoop-master bash -lc '
   hdfs dfs -rm -r -f /output-streaming && \
   hdfs dfs -mkdir -p /input && \
   echo "to be or not to be" > /tmp/text.txt && \
   hdfs dfs -put -f /tmp/text.txt /input && \
   cd /workspace && \
   cp examples/python/wordcount/mapper.py examples/python/wordcount/reducer.py . && \
   hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
      -files mapper.py,reducer.py \
      -mapper "python3 mapper.py" \
      -reducer "python3 reducer.py" \
      -input /input \
      -output /output-streaming && \
   hdfs dfs -cat /output-streaming/part-00000
'
```

## PageRank en Python (Hadoop Streaming)

Un exemple complet (scripts + instructions) est disponible dans `examples/python/pagerank/`.

Pour un essai rapide depuis le conteneur master:

```bash
docker exec -it hadoop-master bash -lc '
   cd /workspace/examples/python/pagerank && \
   export N=4 DAMPING=0.85 PR0=1.0 && \
   hdfs dfs -rm -r -f /pr_input /pr_iter0 /pr_iter1 /pr_iter2 /pr_iter3 || true && \
   hdfs dfs -mkdir -p /pr_input && \
   printf "A\tB,C\nB\tC\nC\tA\nD\tC\n" | hdfs dfs -put - /pr_input/graph.txt && \
   # attach PR0
   hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
      -D stream.num.map.output.key.fields=1 \
      -input /pr_input \
      -output /pr_iter0 \
      -mapper "python3 attach_pr.py" \
      -reducer cat \
      -files attach_pr.py && \
   # 3 iterations
   for i in 1 2 3; do \
      prev=$((i-1)); \
      hdfs dfs -rm -r -f /pr_iter${i} || true; \
      hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
         -D stream.num.map.output.key.fields=1 \
         -input /pr_iter${prev} \
         -output /pr_iter${i} \
         -mapper "python3 mapper.py" \
         -reducer "python3 reducer.py" \
         -files mapper.py,reducer.py \
         -cmdenv N=$N -cmdenv DAMPING=$DAMPING; \
      hdfs dfs -cat /pr_iter${i}/part-* | head -n 10; \
   done && \
   echo "-- Top by PR --" && \
   hdfs dfs -cat /pr_iter3/part-* | sort -k2,2gr | head -n 10
'
```

Notes:
- Exemple minimal: ne redistribue pas la masse des noeuds pendants.
- Voir `examples/python/pagerank/README.md` pour plus de détails.


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
