import React, { useState } from "react";
import ReactCardFlip from "react-card-flip";
import "./Flashcard.css"
  
function Flashcard() {
    const [flip, setFlip] = useState(false);
    return (
        <ReactCardFlip isFlipped={flip} 
            flipDirection="horizontal">
            <button className="card card--front"  onClick={() => setFlip(!flip)}>
                <div className="cardTitleText questionText">Sample Question</div>
                <div className="hr"> </div>
                
            </button>
            <button className="card card--back" onClick={() => setFlip(!flip)}>
                <div className="cardTitleText answerText">Sample Answer</div>
                <div className="hr"></div>
                
            </button>
        </ReactCardFlip>
    );
}
  
export default Flashcard;