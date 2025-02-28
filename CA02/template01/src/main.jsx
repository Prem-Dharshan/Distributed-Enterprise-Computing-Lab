// main.jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  // To be configured
  defaultOptions: {
    queries: {
      retry: 2, // Number of retry attempts for failed queries
      staleTime: 5 * 60 * 1000, // 5 minutes - how long data is considered fresh
      cacheTime: 30 * 60 * 1000, // 30 minutes - how long unused data stays in cache
    },
  },
})

createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* We are telling react that we are using the react query */}
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
