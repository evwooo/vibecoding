import React, { useState } from 'react';

const UnresponsiveButton = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleClick = () => {
    setIsSubmitting(true);
    // Intentionally no timeout reset to keep the button disabled
  };

  return (
    <div className="error-container">
      <h1>Unresponsive UI</h1>
      <div className="error-explanation">
        <h2>What is an Unresponsive UI?</h2>
        <p>
          An unresponsive user interface is one where the user's actions do not provide immediate feedback, leaving them to wonder if their action was registered.
        </p>
        <h2>Common Causes:</h2>
        <ul>
          <li>A long-running process is blocking the main thread.</li>
          <li>Failure to provide feedback during an asynchronous operation (e.g., a network request).</li>
          <li>A bug in the code that prevents an event handler from completing.</li>
        </ul>
        <h2>How to Prevent It:</h2>
        <ul>
          <li>Provide immediate feedback for user actions (e.g., show a loading spinner).</li>
          <li>Disable buttons during submission to prevent multiple clicks.</li>
          <li>Use web workers for long-running computations.</li>
        </ul>
      </div>
      <div className="demo-area">
        <h3>Live Demo</h3>
        <p>This button will become permanently disabled after one click.</p>
        <button onClick={handleClick} disabled={isSubmitting}>
          {isSubmitting ? 'Submitting...' : 'Click Me'}
        </button>
      </div>
    </div>
  );
};

export default UnresponsiveButton;
