import { useState, useEffect } from 'react'

function App() {
  const [todos, setTodos] = useState([])
  const [title, setTitle] = useState('')
  
  const API_URL = 'https://66d389fb6880decad1b4d4cf_lb_944.bm-east.lab.poridhi.io'

  useEffect(() => {
    fetchTodos()
  }, [])

  async function fetchTodos() {
    const res = await fetch(`${API_URL}/todos/`)
    const data = await res.json()
    setTodos(data)
  }

  async function addTodo(e) {
    e.preventDefault()
    await fetch(`${API_URL}/todos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title })
    })
    setTitle('')
    fetchTodos()
  }

  async function deleteTodo(id) {
    await fetch(`${API_URL}/todos/${id}`, { method: 'DELETE' })
    fetchTodos()
  }

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto', padding: '20px' }}>
      <form onSubmit={addTodo}>
        <input 
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Add todo"
          style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
        />
        <button type="submit">Add</button>
      </form>

      {todos.map(todo => (
        <div key={todo.id} style={{ marginTop: '10px', padding: '10px', border: '1px solid #ddd' }}>
          <span>{todo.title}</span>
          <button 
            onClick={() => deleteTodo(todo.id)}
            style={{ float: 'right' }}
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  )
}

export default App