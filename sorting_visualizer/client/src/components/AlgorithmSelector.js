import React from 'react';

const AlgorithmSelector = ({ onAlgorithmChange }) => {
    const algorithms = ['bubbleSort', 'mergeSort', 'quickSort'];

    return (
        <div className="algorithm-selector">
            <h3>Choose algorithms to compare:</h3>
            {algorithms.map(alg => (
                <div key={alg}>
                    <input
                        type="checkbox"
                        id={alg}
                        name={alg}
                        value={alg}
                        onChange={(e) => onAlgorithmChange(e.target.value, e.target.checked)}
                    />
                    <label htmlFor={alg}>{alg.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</label>
                </div>
            ))}
        </div>
    );
};

export default AlgorithmSelector;
