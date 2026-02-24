# Docusaurus Deploy Reference

## Architecture
```
[specs/*.md] → [generate-docs.py] → [docs/] → [Docusaurus Build] → [K8s Pod]
```

## Docusaurus Structure
```
learnflow-docs/
├── docusaurus.config.ts    # Site configuration
├── sidebars.ts             # Sidebar navigation
├── package.json            # Dependencies
├── Dockerfile              # Container build
├── static/                 # Static assets
└── docs/
    ├── intro.md            # Introduction
    ├── architecture/       # System architecture
    ├── api/                # API reference
    ├── skills/             # Skill documentation
    ├── deployment/         # Deployment guides
    └── guides/             # User guides
```

## docusaurus.config.ts
```typescript
import type {Config} from '@docusaurus/types';

const config: Config = {
  title: 'LearnFlow Docs',
  tagline: 'AI-Powered Python Tutoring Platform',
  favicon: 'img/favicon.ico',
  url: 'https://learnflow.dev',
  baseUrl: '/',
  organizationName: 'learnflow',
  projectName: 'learnflow-docs',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  themeConfig: {
    navbar: {
      title: 'LearnFlow',
      items: [
        {to: '/docs/architecture', label: 'Architecture'},
        {to: '/docs/api', label: 'API Reference'},
        {to: '/docs/skills', label: 'Skills Guide'},
        {to: '/docs/deployment', label: 'Deployment'},
      ],
    },
  },
  presets: [['classic', {
    docs: {routeBasePath: '/docs'},
    blog: false,
    theme: {customCss: './src/css/custom.css'},
  }]],
};

export default config;
```

## Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learnflow-docs
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: learnflow-docs
  template:
    metadata:
      labels:
        app: learnflow-docs
    spec:
      containers:
      - name: docs
        image: learnflow-docs:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: learnflow-docs
  namespace: learnflow
spec:
  selector:
    app: learnflow-docs
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
```

## Dockerfile for Docs
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
