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

function Index() {
  return <h1> Index Page </h1>
}

function App() {
  return (
    <BrowserRouter>
      <div>
        <nav>
          <Link to="/add-post">Add Post</Link> |{' '}
          <Link to="/comments">Comments</Link> |{' '}
          <Link to="/todo">Todo List</Link>
        </nav>

        <Routes>
          <Route path='/' element={<Index />} />
          <Route path="/add-post" element={<AddPost />} />
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