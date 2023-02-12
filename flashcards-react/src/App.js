import { useRef, useState, useEffect, createContext } from "react";
import Login from './Login';
import Register from './Register';

export const TokenContext = createContext(null);

function App() {

  const [currentPage, setCurrentPage] = useState('login');

  function changeToRegister(){
    setCurrentPage('register');
  }

  return (
    <main className="App">
      {currentPage=="login"&&<Login  registerLink={changeToRegister}/>}
      {currentPage=="register"&&<Register />}

    </main>
  );
}


export default App;