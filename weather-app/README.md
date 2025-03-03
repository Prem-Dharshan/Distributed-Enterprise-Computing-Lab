# **Weather App 🌤️**  

A simple weather dashboard built with **Vite + React + TypeScript**, using **Tailwind CSS, ShadCN UI, TanStack Query, Axios, and React Router**. The app fetches real-time weather data from [WeatherStack API](https://weatherstack.com/documentation).  

---

## **📌 Features**
✔ Fetches real-time weather data using WeatherStack API  
✔ Allows users to enter a city and view weather details  
✔ Uses **ShadCN Canary + Tailwind v4** for UI styling  
✔ Optimized API requests with **TanStack Query**  
✔ Modern project structure with **Vite + React + TypeScript**  

---

## **🚀 Getting Started**

### **1️⃣ Create the Project**
```sh
# Option 1: Create project in the current directory
npm create vite@latest ./ -- --template react-ts  

# Option 2: Create a new directory named "weather-app"
npm create vite@latest weather-app -- --template react-ts
```

---

### **2️⃣ Install Dependencies**
```sh
cd weather-app
npm install
npm run dev  # Check if it's working in the browser
```

---

### **3️⃣ Install Tailwind CSS**
```sh
npm install tailwindcss @tailwindcss/vite
```
Replace everything in `src/index.css` with:
```css
@import "tailwindcss";
```

---

### **4️⃣ Configure TypeScript**
Modify **`tsconfig.json`**:  
```json
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
```

Modify **`tsconfig.app.json`**:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Install Node.js types:
```sh
npm install -D @types/node
```

---

### **5️⃣ Update `vite.config.ts`**
```ts
import path from "path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

---

### **6️⃣ Install ShadCN Components**
```sh
npx shadcn@latest init
```
- Select **Slate** as the base color  
- Choose **"Use --force"** if prompted for React 19  
- Then, add UI components:
```sh
npx shadcn@latest add button card input skeleton
```

---

### **7️⃣ Install TanStack Query & Axios**
```sh
npm install @tanstack/react-query axios react-router-dom
```

---

### **8️⃣ Setup the App**


#### **🛠️ Environment Variables**
Create a `.env` file in the project root and add your **WeatherStack API Key**:
```
VITE_WEATHERSTACK_API_KEY=your_api_key_here
```
**⚠️ Note:** Restart your server after adding `.env` variables.


---


#### **📌 `main.tsx`**
```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter as Router } from "react-router-dom";
import App from "./App";
import "./index.css"; // Import global styles

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <Router>
        <App />
      </Router>
    </QueryClientProvider>
  </React.StrictMode>
);
```

#### **📌 `App.tsx`**
```tsx
import { Routes, Route } from "react-router-dom";
import CurrentWeather from "./components/CurrentWeather";

function App() {
  return (
    <Routes>
      <Route path="/" element={<CurrentWeather />} />
    </Routes>
  );
}

export default App;
```

---

### **9️⃣ Implement the Weather Dashboard**
#### **📌 `src/components/CurrentWeather.tsx`**
```tsx
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";

const API_URL = "http://api.weatherstack.com/current";
const API_KEY = import.meta.env.VITE_WEATHERSTACK_API_KEY;

const fetchWeather = async (city: string) => {
  if (!city) return null;
  const { data } = await axios.get(API_URL, {
    params: { access_key: API_KEY, query: city },
  });
  return data;
};

const CurrentWeather = () => {
  const [city, setCity] = useState("New York");
  const { data, error, isLoading, refetch } = useQuery({
    queryKey: ["weather", city],
    queryFn: () => fetchWeather(city),
    enabled: false, // Fetch only when user searches
  });

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <Card className="w-full max-w-md p-4 shadow-lg rounded-2xl">
        <CardHeader>
          <CardTitle className="text-xl font-semibold">Weather Dashboard</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2 mb-4">
            <Input
              placeholder="Enter city name"
              value={city}
              onChange={(e) => setCity(e.target.value)}
            />
            <Button onClick={() => refetch()}>Search</Button>
          </div>

          {isLoading && <Skeleton className="h-20 w-full" />}
          {error && <p className="text-red-500">Error fetching data</p>}
          
          {data && data.current && (
            <div className="text-center">
              <h2 className="text-2xl font-bold">{data.location.name}, {data.location.country}</h2>
              <img 
                src={data.current.weather_icons[0]} 
                alt={data.current.weather_descriptions[0]} 
                className="mx-auto my-2"
              />
              <p className="text-lg">{data.current.weather_descriptions[0]}</p>
              <p className="text-4xl font-bold">{data.current.temperature}°C</p>
              <p>Feels like: {data.current.feelslike}°C</p>
              <p>Humidity: {data.current.humidity}%</p>
              <p>Wind: {data.current.wind_speed} km/h {data.current.wind_dir}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CurrentWeather;
```

---

## **🎯 Final Steps**
1️⃣ Run the project  
```sh
npm run dev
```
2️⃣ Open `http://localhost:5173/`  
3️⃣ Enter a city name and press **Search**  

---

## **📜 License**
This project is open-source under the **MIT License**.  

---

Now your **Weather App** is fully set up and running! 🚀 Let me know if you need any modifications. 😃
