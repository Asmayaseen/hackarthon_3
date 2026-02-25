import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'LearnFlow',
  tagline: 'AI-Powered Python Tutoring Platform',
  favicon: 'img/favicon.ico',

  url: 'https://learnflow.ai',
  baseUrl: '/',

  organizationName: 'Asmayaseen',
  projectName: 'learnflow',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/Asmayaseen/hackarthon_3/tree/main/docs-site/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'LearnFlow',
      logo: {
        alt: 'LearnFlow Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://github.com/Asmayaseen/hackarthon_3',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Getting Started', to: '/docs/intro' },
            { label: 'Architecture', to: '/docs/architecture' },
            { label: 'Skills Guide', to: '/docs/skills' },
          ],
        },
        {
          title: 'Platform',
          items: [
            { label: 'API Reference', to: '/docs/api' },
            { label: 'Deployment', to: '/docs/deployment' },
          ],
        },
        {
          title: 'Links',
          items: [
            { label: 'GitHub', href: 'https://github.com/Asmayaseen/hackarthon_3' },
            { label: 'Hackathon III', href: 'https://ggl.link/hackathon-3' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} LearnFlow — Hackathon III`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'docker'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
