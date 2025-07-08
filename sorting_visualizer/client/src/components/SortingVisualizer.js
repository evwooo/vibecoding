import React, { useState, useEffect } from 'react';
import './SortingVisualizer.css';
import { mergeSort } from '../algorithms/mergeSort.js';
import { bubbleSort } from '../algorithms/bubbleSort.js';
import { quickSort } from '../algorithms/quickSort.js';

const SortingVisualizer = ({ algorithm }) => {
    const [array, setArray] = useState([]);

    useEffect(() => {
        resetArray();
    }, []);

    const resetArray = () => {
        const array = [];
        for (let i = 0; i < 100; i++) {
            array.push(randomIntFromInterval(5, 500));
        }
        setArray(array);
    };

    const randomIntFromInterval = (min, max) => {
        return Math.floor(Math.random() * (max - min + 1) + min);
    };

    const animateSort = (animations) => {
        const arrayBars = document.getElementsByClassName('array-bar');
        for (let i = 0; i < animations.length; i++) {
            const isColorChange = i % 3 !== 2;
            if (isColorChange) {
                const [barOneIdx, barTwoIdx] = animations[i];
                const barOneStyle = arrayBars[barOneIdx].style;
                const barTwoStyle = arrayBars[barTwoIdx].style;
                const color = i % 3 === 0 ? 'red' : 'turquoise';
                setTimeout(() => {
                    barOneStyle.backgroundColor = color;
                    barTwoStyle.backgroundColor = color;
                }, i * 10);
            } else {
                setTimeout(() => {
                    const [barOneIdx, newHeight] = animations[i];
                    if(barOneIdx !== -1) {
                        const barOneStyle = arrayBars[barOneIdx].style;
                        barOneStyle.height = `${newHeight}px`;
                    }
                }, i * 10);
            }
        }
    };

    const sort = () => {
        let animations;
        switch (algorithm) {
            case 'bubbleSort':
                animations = bubbleSort(array);
                break;
            case 'mergeSort':
                animations = mergeSort(array);
                break;
            case 'quickSort':
                animations = quickSort(array);
                break;
            default:
                return;
        }
        animateSort(animations);
    };

    return (
        <div className="sorting-visualizer">
            <div className="array-container">
                {array.map((value, idx) => (
                    <div
                        className="array-bar"
                        key={idx}
                        style={{ height: `${value}px` }}
                    ></div>
                ))}
            </div>
            <div className="buttons">
                <button onClick={resetArray}>Generate New Array</button>
                <button onClick={sort}>Sort!</button>
            </div>
        </div>
    );
};

export default SortingVisualizer;
