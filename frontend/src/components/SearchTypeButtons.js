import React from "react";

function SearchTypeButtons({ searchType, handleSearchTypeChange }) {
  return (
    <div>
      <button
        type="button"
        className={searchType === "similarity" ? "selected" : ""}
        onClick={() => handleSearchTypeChange("similarity")}
      >
        Similarity Search
      </button>
      <button
        type="button"
        className={searchType === "keyword" ? "selected" : ""}
        onClick={() => handleSearchTypeChange("keyword")}
      >
        Keyword Search
      </button>
    </div>
  );
}

export default SearchTypeButtons;
