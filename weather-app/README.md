
npm create vite@latest ./  -- --template react-ts
or
npm create vite@latest weather-app  -- --template react-ts

cd weather-app
npm install
npm run dev

check if working in browser

npm install tailwindcss @tailwindcss/vite

Replace everything in src/index.css with the following:

src/index.css
@import "tailwindcss";

Edit tsconfig.json file
The current version of Vite splits TypeScript configuration into three files, two of which need to be edited. Add the baseUrl and paths properties to the compilerOptions section of the tsconfig.json and tsconfig.app.json files:

{
  "files": [],
  "references": [
    {
      "path": "./tsconfig.app.json"
    },
    {
      "path": "./tsconfig.node.json"
    }
  ],
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}


Edit tsconfig.app.json file
Add the following code to the tsconfig.app.json file to resolve paths, for your IDE:

{
  "compilerOptions": {
    // ...
    "baseUrl": ".",
    "paths": {
      "@/*": [
        "./src/*"
      ]
    }
    // ...
  }
}


npm install -D @types/node


Update vite.config.ts
Add the following code to the vite.config.ts so your app can resolve paths without error:

pnpm
npm
yarn
bun
npm install -D @types/node
Copy
vite.config.ts
import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
 
// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})


npx shadcn@latest init
>>
✔ Preflight checks.
✔ Verifying framework. Found Vite.
✔ Validating Tailwind CSS config. Found v4.
✔ Validating import alias.
√ Which color would you like to use as the base color? » Slate
✔ Writing components.json.
✔ Checking registry.
✔ Updating src\index.css
  Installing dependencies.

It looks like you are using React 19. 
Some packages may fail to install due to peer dependency issues in npm (see https://ui.shadcn.com/react-19).

√ How would you like to proceed? » Use --force
✔ Installing dependencies.
✔ Created 1 file:
  - src\lib\utils.ts

Success! Project initialization completed.
You may now add components.


Add Components
You can now start adding components to your project.

npm
npx shadcn@latest add button

Use force for everything

Clear App.css too

npm run dev
and check if shadcn and tailwind is reflected

Lets create a simple dashboard

using https://weatherstack.com/documentation

for sample 
http://api.weatherstack.com/current
    ? access_key = c59a6b299141de998e92177176257efb
    & query = New York


