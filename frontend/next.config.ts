import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  // Pin workspace root so Turbopack doesn't walk up to a parent lockfile
  turbopack: {
    root: path.join(__dirname),
  },
};

export default nextConfig;
