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
      fetch("/data?lang=es").then(res => {
          if (res.ok) {
            res.json().then(idList => {
              setAllCardIds(idList);
              getCard(idList);
            }).catch(e => console.error(e));
          } else {
            console.error(res.statusText);
          }
      });
    }, []);

    const getCard = cards => {
      [[0, setCurrentCard], [1, setNextCard]].forEach(a => {
        fetch(`/data?id=${cards[a[0]]}`).then(res => { 
          if (res.ok) {
            res.json().then(idObj => a[1](idObj)).catch(e => console.error(e));
          } else {
            console.error(res.statusText);
          } 
        });
      });
    }
  
  return (
    <div className="App">
        <Navbar className="Nav" />
        <div className="mainContent">
          <Flashcard className="Flashcard" card={currentCard}/>
        </div>
        
    </div>
  );
}

export default App;
