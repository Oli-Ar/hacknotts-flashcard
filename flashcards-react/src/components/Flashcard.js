import React, { useState, useEffect } from "react";
import ReactCardFlip from "react-card-flip";
import "./Flashcard.css"
  
function Flashcard(props) {
    return (
        <ReactCardFlip isFlipped={props.flip} 
            flipDirection="horizontal">
            <button className="card card--front"  onClick={props.handleFlip}>
                <div className="cardTitleText questionText">{props.card.englishContent}</div>
                <div className="hr"> </div>
            </button>
            <button className="card card--back" onClick={props.handleFlip}>
                <div className="cardTitleText answerText">{props.card.languageContent}</div>
                <div className="hr"></div>
                <button className="audio" onClick={e => {
                    e.stopPropagation();
                    const audio = new Audio(props.card.phoneticAudioLink);
                    audio.play();
                }}>
                    <img className="audioImage" src="https://www.svgrepo.com/show/141310/audio.svg" alt="audio" />
                </button>
                <img className="cardImage" src={props.card.imageLink} alt="Sample" />
            </button>
        </ReactCardFlip>
    );
}
  
export default Flashcard;