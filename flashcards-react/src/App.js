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

    const [allCardIds, setAllCardIds] = useState([])
    const [currentCard, setCurrentCard] = useState({})
    const [nextCard, setNextCard] = useState({})

    const sampleCard =
      {
        engText: "Hello",
        esText: "Hola",
        example: "Hola, como estas?",
        image: "https://t3.ftcdn.net/jpg/03/28/77/18/360_F_328771873_4BLjs8Trc7aUmoeUmFmtLAjJaVGCnlmi.webp"
      }

    useEffect(() => {
      // Using fetch to fetch the api from 
      // flask server it will be redirected to proxy
      fetch("/data?lang=es").then((res) =>
          res.json().then((data) => {
              // Setting a data from api
              setAllCardIds(() => data);
              console.log(currentCard);
          })
      );
    }, []);
  
  return (
    <div className="App">
        <Navbar className="Nav" /> {data.test}
        <div className="mainContent">
          <Flashcard className="Flashcard" card={sampleCard}/>
        </div>
        
    </div>
  );
}

export default App;
