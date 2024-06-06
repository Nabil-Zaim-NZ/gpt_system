import React from "react";

function ExampleQuestions({ questions, handleClick }) {
  return (
    <div className="questions">
      {questions.map((question, index) => (
        <button key={index} onClick={() => handleClick(question)}>
          {question}
        </button>
      ))}
    </div>
  );
}

export default ExampleQuestions;
