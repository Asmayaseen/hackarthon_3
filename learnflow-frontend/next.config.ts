import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/triage/:path*",
        destination: `${process.env.TRIAGE_SERVICE_URL || "http://localhost:8080"}/:path*`,
      },
    ];
  },
};

export default nextConfig;
