import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: ['intro', 'quickstart'],
    },
    {
      type: 'category',
      label: 'Architecture',
      items: ['architecture', 'services', 'kafka-topics', 'mcp-server'],
    },
    {
      type: 'category',
      label: 'Skills Guide',
      items: [
        'skills/overview',
        'skills/agents-md-gen',
        'skills/kafka-k8s-setup',
        'skills/postgres-k8s-setup',
        'skills/fastapi-dapr-agent',
        'skills/mcp-code-execution',
        'skills/nextjs-k8s-deploy',
        'skills/docusaurus-deploy',
      ],
    },
    {
      type: 'category',
      label: 'API Reference',
      items: ['api/triage', 'api/concepts', 'api/progress', 'api/mcp'],
    },
    {
      type: 'category',
      label: 'Deployment',
      items: ['deployment/local', 'deployment/kubernetes', 'deployment/argocd'],
    },
    {
      type: 'category',
      label: 'User Guides',
      items: ['guides/student', 'guides/teacher'],
    },
  ],
};

export default sidebars;
