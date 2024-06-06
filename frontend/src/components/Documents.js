import React from "react";
import "../css/documents.css";

function Documents({ documents }) {
  return (
    <div className="documents">
      {documents.length > 0 ? (
        documents.map((document, index) => (
          <div key={index} className="document-card">
            <img src={document.top_image} alt="" />
            <h3 className="title">{document.title}</h3>
            <p className="paragraph">{document.paragraph}</p>
            <a
              href={document.link}
              target="_blank"
              rel="noopener noreferrer"
              className="read-more"
            >
              Read more
            </a>
            <p className="relevance">Relevance: {document.relevance}</p>
          </div>
        ))
      ) : (
        <p className="no-results">
          No results found. Try refining your keywords.
        </p>
      )}
    </div>
  );
}

export default Documents;
