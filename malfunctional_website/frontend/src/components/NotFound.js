import React from 'react';

const NotFound = () => {
  return (
    <div className="error-container">
      <h1>404 - Not Found</h1>
      <div className="error-explanation">
        <h2>What is a 404 Error?</h2>
        <p>
          A 404 error is an HTTP status code that means the page you were trying to reach on a website couldn't be found on their server.
        </p>
        <h2>Common Causes:</h2>
        <ul>
          <li>The URL was typed incorrectly.</li>
          <li>The page was moved or deleted.</li>
          <li>There is a broken link from another page.</li>
        </ul>
        <h2>How to Prevent It:</h2>
        <ul>
          <li>Double-check URLs before linking to them.</li>
          <li>Implement 301 redirects for pages that have moved permanently.</li>
          <li>Create a custom, helpful 404 page to guide users.</li>
        </ul>
      </div>
      <div className="demo-area">
        <h3>Live Demo</h3>
        <p>You are here! This page is the custom 404 error page for this site.</p>
      </div>
    </div>
  );
};

export default NotFound;
