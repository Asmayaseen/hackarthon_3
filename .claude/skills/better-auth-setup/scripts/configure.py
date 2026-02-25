#!/usr/bin/env python3
"""Generate Better Auth configuration for LearnFlow."""
import sys
config = """
# Better Auth config (add to learnflow-frontend/src/lib/auth.ts)
import { betterAuth } from "better-auth";
export const auth = betterAuth({
  database: { provider: "pg", url: process.env.DATABASE_URL },
  emailAndPassword: { enabled: true },
  session: { expiresIn: 60 * 60 * 24 * 7 },
  user: { additionalFields: { role: { type: "string", defaultValue: "student" } } }
});
"""
print(config)
print("✓ Better Auth configuration generated")
sys.exit(0)
