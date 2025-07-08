import React, { useState } from 'react';
import './App.css';
import SortingVisualizer from './components/SortingVisualizer';
import AlgorithmSelector from './components/AlgorithmSelector';
import CodeViewer from './components/CodeViewer';

function App() {
  const [algorithms, setAlgorithms] = useState([]);
  const [activeAlgorithm, setActiveAlgorithm] = useState(null);

  const handleAlgorithmChange = (algorithm, isSelected) => {
    if (isSelected) {
      setAlgorithms(prev => [...prev, algorithm]);
    } else {
      setAlgorithms(prev => prev.filter(alg => alg !== algorithm));
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Sorting Algorithm Visualizer</h1>
      </header>
      <main className="App-main">
        <div className="visualizer-container">
          <AlgorithmSelector onAlgorithmChange={handleAlgorithmChange} />
          <div className="visualizers">
            {algorithms.map(alg => (
              <div key={alg} onMouseEnter={() => setActiveAlgorithm(alg)}>
                <h2>{alg.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</h2>
                <SortingVisualizer algorithm={alg} />
              </div>
            ))}
          </div>
        </div>
        <div className="code-container">
          <CodeViewer algorithm={activeAlgorithm} />
        </div>
      </main>
    </div>
  );
}

export default App;
