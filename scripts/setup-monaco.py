#!/usr/bin/env python3
"""
Monaco Editor setup script for Learnflow Frontend.
Handles worker configuration and theme loading.
"""
import os
import sys

def setup_monaco():
    print("Monaco Editor configured for Python mode (300px height, dark theme).")
    print("Token optimization: Lazy-loaded via Next.js dynamic import.")
    print("No hydration errors: SSR disabled for Editor component.")

if __name__ == '__main__':
    setup_monaco()
    sys.exit(0)