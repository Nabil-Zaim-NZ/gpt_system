import React, { useEffect, useState } from "react";
import "./App.css";
import Documents from "./components/Documents";
import ExampleQuestions from "./components/ExampleQuestions.js";
import PopUp from "./components/PopUp";
import SearchForm from "./components/SearchForm.js";
import SearchTypeButtons from "./components/SearchTypeButtons.js";

function App() {
  const [questions, setQuestions] = useState([]);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({
    similarity_results: [],
    keyword_results: [],
  });
  const [searchType, setSearchType] = useState("similarity");
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const fetchQuestions = async () => {
      const response = await fetch("http://127.0.0.1:5000/example_questions");
      const data = await response.json();
      setQuestions(data.questions);
    };

    fetchQuestions();
  }, []);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleClick = async (question) => {
    setQuery(question);
    await handleSubmit();
  };

  const handleSearchTypeChange = (type) => {
    setSearchType(type);
  };

  const handleSubmit = async (e) => {
    if (e) {
      e.preventDefault();
    }
    if (query) {
      const response = await fetch("http://127.0.0.1:5000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, searchType }),
      });
      const data = await response.json();
      const similarityEmpty = data.similarity_results.length === 0;
      const keywordEmpty = data.keyword_results.length === 0;
      if (similarityEmpty && keywordEmpty) {
        setShowPopup(true);
        setTimeout(() => setShowPopup(false), 2000);
      }
      if (similarityEmpty && !keywordEmpty) {
        setSearchType("keyword");
      }
      if (!similarityEmpty && keywordEmpty) {
        setSearchType("similarity");
      }
      setResults(data);
    }
  };

  return (
    <div className="App">
      <h1>Search Interface</h1>
      <SearchForm
        query={query}
        handleQueryChange={handleQueryChange}
        handleSubmit={handleSubmit}
      />
      {showPopup && (
        <PopUp message="Zero relevance to contents. Please, try with new search." />
      )}
      <h2>Example Questions</h2>
      <ExampleQuestions questions={questions} handleClick={handleClick} />
      <h3>Choose the search technique: </h3>
      <SearchTypeButtons
        searchType={searchType}
        handleSearchTypeChange={handleSearchTypeChange}
      />
      <Documents
        documents={
          searchType === "similarity"
            ? results.similarity_results
            : results.keyword_results
        }
      />
    </div>
  );
}

export default App;
