import './App.css';
import React, { useState, useEffect } from "react"
import Navbar from "./components/Navbar"
import Flashcard from "./components/Flashcard"

function App() {
    const [data, setdata] = useState({
        name: "",
        age: 0,
        date: "",
        programming: "",
    });

    useEffect(() => {
      // Using fetch to fetch the api from 
      // flask server it will be redirected to proxy
      fetch("/data").then((res) =>
          res.json().then((data) => {
              // Setting a data from api
              setdata({
                test: data.test
              });
          })
      );
    }, []);
  
  return (
    <div className="App">
        <Navbar className="Nav" /> {data.test}
        <div className="mainContent">
          <Flashcard className="Flashcard" />
        </div>
        
    </div>
  );
}

export default App;
