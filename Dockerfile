FROM openjdk:8-jre-slim

ENV HADOOP_VERSION=3.3.6 \
    HADOOP_HOME=/opt/hadoop \
    HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop \
    JAVA_HOME=/usr/local/openjdk-8 \
    PATH=$PATH:/opt/hadoop/bin:/opt/hadoop/sbin

RUN apt-get update && apt-get install -y curl bash procps supervisor && rm -rf /var/lib/apt/lists/* \
 && curl -L https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
 | tar -xz -C /opt && mv /opt/hadoop-${HADOOP_VERSION} ${HADOOP_HOME}

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY core-site.xml hdfs-site.xml yarn-site.xml mapred-site.xml ${HADOOP_CONF_DIR}/

ENTRYPOINT ["/entrypoint.sh"]
