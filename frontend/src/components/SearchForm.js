import React from "react";

function SearchForm({ query, handleQueryChange, handleSubmit }) {
  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={handleQueryChange}
        placeholder="Enter your query"
      />
      <button type="submit">Search</button>
    </form>
  );
}

export default SearchForm;
