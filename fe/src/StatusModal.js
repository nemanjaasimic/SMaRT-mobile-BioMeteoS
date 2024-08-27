// src/StatusModal.js
import React from 'react';
import './StatusModal.css';

function StatusModal({ show, onClose, status }) {
    if (!show) {
        return null;
    }

    return (
        <div className="status-modal">
            <div className="status-modal-content">
                <h2>Measurement Status</h2>
                <pre>{JSON.stringify(status, null, 2)}</pre>
                <button onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default StatusModal;
