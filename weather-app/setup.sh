#!/bin/bash

# Check if project name is provided
if [ -z "$1" ]; then
  echo "Please provide a project name."
  exit 1
fi

# Set project name from command-line argument
PROJECT_NAME="$1"

# Create a new Vite project with React template
npm create vite@latest "$PROJECT_NAME" -- --template react-ts

# Change directory to the new project
cd "$PROJECT_NAME"

# Install necessary dependencies
npm install axios @tanstack/react-query @tanstack/react-query-devtools react-router-dom dotenv

# Install tailwind and make the necessary configurations
npm install tailwindcss @tailwindcss/vite

npm install -D @types/node

cat << EOF > vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from "path"
import dotenv from "dotenv";
dotenv.config();

export default defineConfig({
  plugins: [tailwindcss(), react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
EOF

cat << EOF > src/index.css
@import "tailwindcss";
EOF

cat << EOF > tsconfig.json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
EOF

cat << EOF > tsconfig.app.json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedSideEffectImports": true,

    // shadcn
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
  },
  "include": ["src"]
}
EOF

npx shadcn@latest init

echo "Project setup complete!"
