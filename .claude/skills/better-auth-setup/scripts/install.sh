#!/bin/bash
set -e
cd learnflow-frontend
npm install better-auth @better-auth/next
echo "✓ Better Auth installed in learnflow-frontend"
cd ..
pip install python-jose[cryptography] passlib[bcrypt] -q
echo "✓ JWT dependencies installed for backend services"
