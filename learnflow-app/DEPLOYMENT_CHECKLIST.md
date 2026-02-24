# LearnFlow Core Services - Deployment Checklist

## Pre-Deployment Requirements

### ✅ Prerequisites (Must Complete)

- [ ] **Minikube Running**
  ```bash
  minikube start --cpus=4 --memory=8192 --driver=docker
  ```

- [ ] **kubectl Context**
  ```bash
  kubectl config current-context  # Should show minikube
  ```

- [ ] **OpenAI API Key**
  - Get API key from: https://platform.openai.com/api-keys
  - Update in: `k8s/components/openai-secret.yaml`
  - Encode to Base64: `echo -n "YOUR_API_KEY" | base64`

- [ ] **Helm Installed** (for Kafka deployment)
  ```bash
  helm version
  ```

### 📦 Deployment Steps

**Step 1: Update OpenAI Secret**
```bash
cd /mnt/d/hackathon-3-all-phases/learnflow-app

# Edit the secret file and replace the placeholder
nano k8s/components/openai-secret.yaml
# Replace: api-key: UExBQ0VIT0xERVJfQkFTRTY0X0VOQ09ERURfQVBJX0tFWQ==
# With: api-key: <your-base64-encoded-api-key>
```

**Step 2: Run Deployment Script**
```bash
./deploy.sh
```

**Step 3: Verify Deployment**
```bash
# Check all pods are running
kubectl get pods -n learnflow

# Expected output:
# NAME                               READY   STATUS    RESTARTS   AGE
# concepts-service-xxxx              2/2     Running   0          2m
# concepts-service-xxxx              2/2     Running   0          2m
# triage-service-xxxx                2/2     Running   0          2m
# triage-service-xxxx                2/2     Running   0          2m

# Check services
kubectl get svc -n learnflow

# Check Dapr sidecars
kubectl logs -l app=triage-service -n learnflow -c daprd
kubectl logs -l app=concepts-service -n learnflow -c daprd
```

**Step 4: Port Forward for Testing**
```bash
# Terminal 1 - Triage Service
kubectl port-forward svc/triage-service 8080:80 -n learnflow

# Terminal 2 - Concepts Service (optional)
kubectl port-forward svc/concepts-service 8081:80 -n learnflow
```

**Step 5: Test End-to-End Flow**
```bash
# Test Triage Service
 curl -X POST http://localhost:8080/query \
   -H "Content-Type: application/json" \
   -d '{
     "student_id": "student-123",
     "query_text": "How do for loops work in Python?",
     "student_level": "beginner"
   }'

# Expected Response:
# {
#   "classification": "explain",
#   "confidence": 0.85,
#   "reason": "Student is asking about Python syntax",
# }

# Check Concepts Service logs to see if it processed the message
kubectl logs -l app=concepts-service -n learnflow -c concepts-service
```

**Step 6: Monitor Events in Kafka**
```bash
# List Kafka topics
kubectl exec -n kafka -it kafka-cluster-kafka-0 -- kafka-topics.sh \
  --list \
  --bootstrap-server localhost:9092

# Expected topics:
# learning.query.explain
# learning.query.routed
# learning.query.unclassified
```

### 🐛 Troubleshooting

**Problem: Pods stuck in Init/ContainerCreating**
```bash
# Check events
kubectl get events -n learnflow --sort-by='.lastTimestamp'

# Common causes:
# - Image not found: Ensure images loaded into Minikube
# - Secret missing: Check openai-secret.yaml applied
# - Kafka not ready: Wait for Kafka pods to be Running
```

**Problem: Dapr sidecar not connecting**
```bash
# Check Dapr logs
kubectl logs -l app=triage-service -n learnflow -c daprd

# Verify Dapr is installed in cluster
kubectl get pods -n dapr-system
```

**Problem: OpenAI API errors**
```bash
# Check service logs
kubectl logs -l app=triage-service -n learnflow -c triage-service

# Verify API key
kubectl get secret openai-secret -n learnflow -o yaml
```

**Problem: Kafka publish failing**
```bash
# Check Kafka connectivity from pod
kubectl exec -n learnflow -it <triage-pod> -- curl http://kafka-cluster-kafka-bootstrap.kafka:9092

# Check Dapr component status
kubectl get components -n learnflow
```

**Problem: High latency / timeouts**
```bash
# Check resource limits
kubectl top pods -n learnflow

# Increase resources in deployment YAML if needed
# requests: memory: "256Mi", cpu: "200m"
```

### ✅ Post-Deployment Verification

**Checklist**:

- [ ] All pods in "Running" state (4 pods total)
- [ ] All services have Endpoints assigned
- [ ] Dapr sidecars show "Connected to Kafka" in logs
- [ ] OpenAI API calls succeed (200 responses)
- [ ] Kafka topics created and receiving messages
- [ ] End-to-end flow tested successfully
- [ ] Logs show no errors

**Success Metrics**:

- Triage classification: < 2 seconds response time
- Concepts explanation: < 3 seconds generation time
- Kafka publish: < 500ms latency
- Pod restart count: 0
- Memory usage: < 256Mi per pod
- CPU usage: < 200m per pod

### 📝 Artifacts After Deployment

**Logs**:
```bash
# View all logs
kubectl logs -l app=triage-service -n learnflow -f
kubectl logs -l app=concepts-service -n learnflow -f
```

**Metrics**:
```bash
# Port forward Dapr dashboard (in separate terminal)
kubectl port-forward -n dapr-system svc/dapr-dashboard 8080:8080
# Open: http://localhost:8080
```

**Cleanup**:
```bash
# Delete everything
kubectl delete namespace learnflow
kubectl delete namespace kafka

# Or use the deployment script's cleanup mode
./deploy.sh --cleanup
```

## Architecture Reference

- **Event-Driven Pattern**: `/mnt/d/hackathon-3-all-phases/history/adr/001-event-driven-architecture-with-dapr-kafka.md`
- **OpenAI Integration**: `/mnt/d/hackathon-3-all-phases/history/adr/002-openai-integration-for-agent-intelligence.md`
- **Specification**: `/mnt/d/hackathon-3-all-phases/specs/1-learnflow-core-services/spec.md`
- **Constitution**: `/mnt/d/hackathon-3-all-phases/.specify/memory/constitution.md`

## Support

If deployment fails:
1. Check all prerequisites are met
2. Review logs from failed pods
3. Verify Kafka is running
4. Ensure OpenAI API key is valid
5. Check Dapr component configuration
6. Verify network connectivity between pods

For help: Review ADRs for architectural decisions and rationale
