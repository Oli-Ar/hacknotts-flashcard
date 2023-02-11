import React, { useState } from "react";
import ReactCardFlip from "react-card-flip";
import "./Flashcard.css"
  
function Flashcard(props) {
    const [flip, setFlip] = useState(false);
    return (
        <ReactCardFlip isFlipped={flip} 
            flipDirection="horizontal">
            <button className="card card--front"  onClick={() => setFlip(!flip)}>
                <div className="cardTitleText questionText">{props.card.engText}</div>
                <div className="hr"> </div>
                
            </button>
            <button className="card card--back" onClick={() => setFlip(!flip)}>
                <div className="cardTitleText answerText">{props.card.esText}</div>
                <div className="exampleText">
                {props.card.example}
                </div>
                <div className="hr"></div>
                
                <img className="cardImage" src={props.card.image} alt="Sample" />
            </button>
        </ReactCardFlip>
    );
}
  
export default Flashcard;