# PageRank en Python (Hadoop Streaming)

Ce dossier contient une implémentation minimaliste de PageRank via Hadoop Streaming en Python.

- `attach_pr.py`: attache un PR initial (PR0) à chaque ligne de la liste d'adjacence
- `mapper.py`: distribue le rang courant aux voisins et passe la structure du graphe
- `reducer.py`: agrège les contributions, applique l'amortissement et reconstruit l'état

Format d'entrée attendu (HDFS, une ligne par noeud):
```
source\tn1,n2,n3
```

Format d'état après initialisation/itérations:
```
node\tPR\tn1,n2,n3
```

## Exécution rapide (depuis le conteneur master)

Variables:
- N: nombre total de noeuds du graphe
- DAMPING: facteur d'amortissement (par défaut 0.85)
- PR0: PR initial par noeud (par défaut 1.0 si non fourni)

Exemple avec un petit graphe de 4 noeuds:
```
Voir `sample_graph.txt`:
A\tB,C
B\tC
C\tA
D\tC
```

### 1) Préparer les fichiers
- Copiez ces scripts dans HDFS via `-files` (le job les localise par basename)

### 2) Initialiser l'état (attacher PR0)
```
export N=4 DAMPING=0.85 PR0=1.0
hdfs dfs -rm -r -f /pr_input /pr_iter0 /pr_iter1 /pr_iter2 /pr_iter3 /pr_out || true
hdfs dfs -mkdir -p /pr_input
hdfs dfs -put -f sample_graph.txt /pr_input/graph.txt

# Attacher PR initial
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -D stream.num.map.output.key.fields=1 \
  -input /pr_input \
  -output /pr_iter0 \
  -mapper "python3 attach_pr.py" \
  -reducer cat \
  -file attach_pr.py
```

### 3) Lancer K itérations
```
for i in 1 2 3; do
  prev=$((i-1))
  hdfs dfs -rm -r -f /pr_iter${i} || true
  hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -D stream.num.map.output.key.fields=1 \
    -input /pr_iter${prev} \
    -output /pr_iter${i} \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file mapper.py -file reducer.py \
    -cmdenv N=$N -cmdenv DAMPING=$DAMPING
  hdfs dfs -cat /pr_iter${i}/part-* | head -n 10
done
```

### 4) Résultats triés (optionnel)
```
hdfs dfs -cat /pr_iter3/part-* | sort -k2,2gr | head -n 10
```

Notes:
- Cette version ignore la redistribution de la masse « dangling » (noeuds sans sorties). Pour un graphe sans noeuds pendants, le résultat est correct; sinon, la masse manquante n'est pas réinjectée.
- Assurez-vous que `N` correspond bien au nombre de noeuds distincts.
