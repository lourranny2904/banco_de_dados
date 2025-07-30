import { useState } from 'react'
import './App.css'
import Listas from './componentes/Listas'
import Login from './componentes/Login'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      {/* <Login></Login> */}
      <Listas></Listas>
    </>
  )
}

export default App
