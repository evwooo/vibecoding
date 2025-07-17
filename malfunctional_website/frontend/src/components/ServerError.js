import React, { useState, useEffect } from 'react';

const ServerError = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const triggerError = () => {
    setLoading(true);
    fetch('http://localhost:5001/api/server-error')
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  };

  return (
    <div className="error-container">
      <h1>500 - Internal Server Error</h1>
      <div className="error-explanation">
        <h2>What is a 500 Error?</h2>
        <p>
          A 500 Internal Server Error is a generic error message, given when an unexpected condition was encountered and no more specific message is suitable.
        </p>
        <h2>Common Causes:</h2>
        <ul>
          <li>A bug in the server-side code.</li>
          <li>Database connection issues.</li>
          <li>Problems with server configuration.</li>
        </ul>
        <h2>How to Prevent It:</h2>
        <ul>
          <li>Implement robust error handling and logging on the server.</li>
          <li>Thoroughly test new code before deploying.</li>
          <li>Use a tool to monitor your application for errors.</li>
        </ul>
      </div>
      <div className="demo-area">
        <h3>Live Demo</h3>
        <button onClick={triggerError} disabled={loading}>
          {loading ? 'Loading...' : 'Trigger 500 Error'}
        </button>
        {error && <p style={{ color: 'var(--error-color)' }}>Error: {error}</p>}
      </div>
    </div>
  );
};

export default ServerError;
