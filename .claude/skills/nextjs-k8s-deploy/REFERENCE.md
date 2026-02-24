# Next.js Kubernetes Deploy Reference

## Architecture
```
[User Browser] → [K8s Ingress / Port-Forward] → [learnflow-frontend:3000]
                                                        ↓
                                               [API Routes (/api/*)]
                                                        ↓
                                        [triage-service.learnflow:80]
```

## Dockerfile Pattern (Multi-stage)
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
```

## next.config.ts Requirements
```typescript
// Enable standalone output for Docker
const nextConfig = {
  output: 'standalone',
  // API proxy to backend services
  async rewrites() {
    return [
      {
        source: '/api/triage/:path*',
        destination: `${process.env.TRIAGE_SERVICE_URL}/api/triage/:path*`,
      },
      {
        source: '/api/progress/:path*',
        destination: `${process.env.PROGRESS_SERVICE_URL}/api/progress/:path*`,
      },
    ]
  },
}
```

## Kubernetes Manifest
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learnflow-frontend
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: learnflow-frontend
  template:
    metadata:
      labels:
        app: learnflow-frontend
    spec:
      containers:
      - name: frontend
        image: learnflow-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: TRIAGE_SERVICE_URL
          value: "http://triage-service.learnflow.svc.cluster.local"
        - name: PROGRESS_SERVICE_URL
          value: "http://progress-service.learnflow.svc.cluster.local"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: learnflow-frontend
  namespace: learnflow
spec:
  selector:
    app: learnflow-frontend
  ports:
  - port: 3000
    targetPort: 3000
  type: ClusterIP
```

## Troubleshooting
```bash
# Check pod logs
kubectl logs -l app=learnflow-frontend -n learnflow --tail=50

# Check pod events
kubectl describe pod -l app=learnflow-frontend -n learnflow

# Restart deployment
kubectl rollout restart deployment/learnflow-frontend -n learnflow

# Check build issues (run locally)
cd learnflow-frontend && npm run build
```
