import React from 'react';
import './CodeViewer.css';
import { bubbleSortCode } from '../algorithms/bubbleSort';
import { mergeSortCode } from '../algorithms/mergeSort';
import { quickSortCode } from '../algorithms/quickSort';

const CodeViewer = ({ algorithm }) => {
    const getCode = () => {
        switch (algorithm) {
            case 'bubbleSort':
                return bubbleSortCode;
            case 'mergeSort':
                return mergeSortCode;
            case 'quickSort':
                return quickSortCode;
            default:
                return '';
        }
    };

    return (
        <div className="code-viewer">
            <pre>
                <code>{getCode()}</code>
            </pre>
        </div>
    );
};

export default CodeViewer;
