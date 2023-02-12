import './App.css';
import React, { useState, useEffect } from "react"
import Navbar from "./components/Navbar"
import Flashcard from "./components/Flashcard"

function App() {
    const [allCardIds, setAllCardIds] = useState([])
    const [currentCard, setCurrentCard] = useState({})
    const [nextCard, setNextCard] = useState({})

    useEffect(() => {
      // Using fetch to fetch the api from 
      // flask server it will be redirected to proxy
      if (allCardIds.length === 0) {
        fetch("/data?lang=es").then(res => {
            res.json().then(idList => setAllCardIds(() => idList)).catch(e => console.log(e));
        });
      }

      fetch(`/data?id=${allCardIds[3]}`).then(res => {
        res.json().then(idObj => setCurrentCard(() => idObj)).catch(e => console.log(e))
      })
    }, [allCardIds]);
  
  return (
    <div className="App">
        <Navbar className="Nav" />
        <div className="mainContent">
          <Flashcard className="Flashcard" card={currentCard}/>
          <button className="nextButton">
            <div className="buttonText">
              Next Card
            </div>
          </button>
        </div>
        
    </div>
  );
}

export default App;
