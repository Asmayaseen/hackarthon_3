#!/bin/bash
set -e

kubectl create namespace kafka-ns --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f https://github.com/strimzi/strimzi-kafka-operator/releases/download/strimzi-0.41.0/strimzi-cluster-operator-0.41.0.yaml
sleep 30
cat <<EOF | kubectl apply -f -
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: learnflow-kafka
  namespace: kafka-ns
spec:
  kafka:
    version: 3.8.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
EOF
echo "✓ Kafka deployed in kafka-ns"
kubectl -n kafka-ns get kafka