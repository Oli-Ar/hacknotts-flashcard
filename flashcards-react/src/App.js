import { useRef, useState, useEffect, createContext } from "react";
import Login from './Login';

export const TokenContext = createContext(null);

function App() {

  return (
    <main className="App">
      <Login />
    </main>
  );
}


export default App;