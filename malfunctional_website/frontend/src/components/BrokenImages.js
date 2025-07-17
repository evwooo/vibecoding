import React from 'react';

const BrokenImages = () => {
  return (
    <div className="error-container">
      <h1>Broken Images</h1>
      <div className="error-explanation">
        <h2>What are Broken Images?</h2>
        <p>
          A broken image icon appears when an image file cannot be loaded by the browser.
        </p>
        <h2>Common Causes:</h2>
        <ul>
          <li>The image file path is incorrect.</li>
          <li>The image file was deleted or moved.</li>
          <li>There is a typo in the image file name or extension.</li>
        </ul>
        <h2>How to Prevent It:</h2>
        <ul>
          <li>Always double-check image paths.</li>
          <li>Use relative paths to images when possible.</li>
          <li>Make sure images are included in your project's build process.</li>
        </ul>
      </div>
      <div className="demo-area">
        <h3>Live Demo</h3>
        <p>This image has an incorrect source:</p>
        <img src="/path/to/nonexistent-image.png" alt="A broken image" className="broken-image" />
      </div>
    </div>
  );
};

export default BrokenImages;
