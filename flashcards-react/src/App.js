import './App.css';
import React, { useState, useEffect, useRef } from "react"
import Navbar from "./components/Navbar"
import Flashcard from "./components/Flashcard"

function App() {
    const [allCardIds, setAllCardIds] = useState([])
    const [currentCard, setCurrentCard] = useState({})
    const [nextCard, setNextCard] = useState({})

    const [flip, setFlip] = useState(false)

    const allCardIdsRef = useRef([]);

    function handleFlip() {
      setFlip(!flip)
    }

    function sleep(ms) { 
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    async function handleNext() {
      if (flip){
        setFlip(false);
        await sleep(500);
      }
      setCurrentCard(nextCard)
      getCard(allCardIds, +localStorage.getItem("currentCard")+1)
    }

    useEffect(() => {
      fetch("/data?lang=es").then(res => {
          if (res.ok) {
            res.json().then(idList => {
              allCardIdsRef.current = idList;
              setAllCardIds(idList);
              getCard(idList, idList.length);
            }).catch(e => console.error(e));
          } else {
            console.error(res.statusText);
          }
      });
    }, []);

    const getCard = (cards, i) => {
      console.log(i % cards.length);
      localStorage.setItem("currentCard", i);
      [[i, setCurrentCard], [i+1, setNextCard]].forEach(a => {
        fetch(`/data?id=${cards[a[0] % allCardIdsRef.current.length]}`).then(res => { 
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
          <Flashcard className="Flashcard" card={currentCard} flip={flip} handleFlip={handleFlip}/>
          <button className="nextButton" onClick={handleNext/*()=>getCard(allCardIds, +localStorage.getItem("currentCard")+1)*/}>
            <div className="buttonText">
              Next Card
            </div>
          </button>
        </div>
        
    </div>
  );
}

export default App;
