#!/usr/bin/env bash
set -e

# Ensure Java and Hadoop are available
export JAVA_HOME=${JAVA_HOME:-/usr/local/openjdk-8}
export HADOOP_HOME=${HADOOP_HOME:-/opt/hadoop}
export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-/opt/hadoop/etc/hadoop}
export PATH="$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin"

: ${NN_HOST:=master}
: ${REPLICATION:=2}

sed -i "s|__NN_HOST__|${NN_HOST}|g" ${HADOOP_CONF_DIR}/core-site.xml
sed -i "s|__REPL__|${REPLICATION}|g"  ${HADOOP_CONF_DIR}/hdfs-site.xml

if [ "$ROLE" = "master" ] && [ ! -d "/hadoop/nn/current" ]; then
  mkdir -p /hadoop/nn /hadoop/dn
  hdfs namenode -format -nonInteractive -force
fi
mkdir -p /hadoop/dn

exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
