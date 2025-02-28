Tanstack setup

```bash
npm i @tanstack/react-query
```

```jsx
// main.jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <QueryClientProvider>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)
```

Refer this https://tanstack.com/query/latest/docs/framework/react/quick-start
https://jsonplaceholder.typicode.com/guide/

Create a function to handle the api service defined in the services/todos.js

Then use the usequery hook to destructure data and neccessary stuff at components/TodoList.jsx

Include the TodoList compoennt in the App.jsx


cant use enabled prop if using useSuspenseQuery


Use useQuery to handle GET requests, This facilitates the error and loading state management and also the useEffect automatically
queryKey is used for cahcing a request uniquely, makes app faster
queryFn is the fetch fn, can be axios or fetch()
tanstack != axios or fetch, its just a easier state management tool for apis
For params, refer https://tanstack.com/query/v5/docs/framework/react/reference/useQuery
The `refetch` manually fetches instead of automatically fetching as per queryClient config


Lets explore useMutation hook, basically used for PUT, PATCH, DELETE
We



npm install react-router-dom
Let's learn React Router with your existing App component! React Router is a powerful library for handling navigation and routing in React applications. I'll guide you through setting it up step-by-step.

First, you'll need to install React Router:
```bash
npm install react-router-dom
```

Here's how you can modify your code to use React Router:

```jsx
import './App.css'
import { AddPost } from './component/AddPost'
import PostComments from './component/PostComments'
import TodoList from './component/TodoList'
// Import BrowserRouter, Routes, and Route from react-router-dom
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter> {/* Wrap everything in BrowserRouter */}
      <div>
        {/* Navigation Links */}
        <nav>
          <Link to="/">Add Post</Link> |{' '}
          <Link to="/comments">Comments</Link> |{' '}
          <Link to="/todo">Todo List</Link>
        </nav>

        {/* Define your routes */}
        <Routes>
          <Route path="/" element={<AddPost />} />
          <Route path="/comments" element={<PostComments />} />
          <Route path="/todo" element={<TodoList />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
```

Let's break down the key concepts:

1. **BrowserRouter**
- Wraps your entire application
- Enables routing functionality
- Should be at the top level of your app

2. **Routes and Route**
- `<Routes>` is a container for all your route definitions
- `<Route>` defines a single route with:
  - `path`: URL path
  - `element`: Component to render

3. **Link**
- Creates navigation links
- Replaces `<a>` tags to prevent full page reloads
- Uses `to` prop for the destination path

Here's a more advanced example with additional features:

```jsx
import './App.css'
import { AddPost } from './component/AddPost'
import PostComments from './component/PostComments'
import TodoList from './component/TodoList'
import { BrowserRouter, Routes, Route, Link, useParams, Navigate } from 'react-router-dom'

// A component with URL parameters
function PostDetail() {
  const { id } = useParams() // Get URL parameters
  return <h2>Post ID: {id}</h2>
}

function NotFound() {
  return <h2>404 - Page Not Found</h2>
}

function App() {
  return (
    <BrowserRouter>
      <div>
        <nav>
          <Link to="/">Add Post</Link> |{' '}
          <Link to="/comments">Comments</Link> |{' '}
          <Link to="/todo">Todo List</Link>
        </nav>

        <Routes>
          <Route path="/" element={<AddPost />} />
          <Route path="/comments" element={<PostComments />} />
          <Route path="/todo" element={<TodoList />} />
          {/* Dynamic route with parameter */}
          <Route path="/post/:id" element={<PostDetail />} />
          {/* Catch-all route for 404 */}
          <Route path="*" element={<NotFound />} />
          {/* Redirect example */}
          <Route path="/old-route" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
```

Additional useful features:

1. **Nested Routes**
```jsx
<Route path="/comments" element={<PostComments />}>
  <Route path=":id" element={<CommentDetail />} />
</Route>
```

2. **Programmatic Navigation**
```jsx
import { useNavigate } from 'react-router-dom'

function AddPost() {
  const navigate = useNavigate()
  
  const handleSubmit = () => {
    // After submitting
    navigate('/comments')
  }
}
```

3. **Query Parameters**
```jsx
import { useSearchParams } from 'react-router-dom'

function TodoList() {
  const [searchParams, setSearchParams] = useSearchParams()
  const filter = searchParams.get('filter') // e.g., ?filter=active
}
```
