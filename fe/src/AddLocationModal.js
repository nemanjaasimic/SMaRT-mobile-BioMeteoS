import React, { useState } from 'react';
import './AddLocationModal.css';

function AddLocationModal({ show, onClose }) {
    const [locationName, setLocationName] = useState('');

    const handleAddLocation = async () => {
        const response = await fetch('http://192.168.0.114:5000/locations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: locationName })
        });

        if (response.ok) {
            alert('Location added successfully.');
            setLocationName('');
            onClose();
        } else {
            alert('Failed to add location.');
        }
    };

    if (!show) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>Add Location</h2>
                <label>Location Name:</label>
                <input value={locationName} onChange={(e) => setLocationName(e.target.value)} />
                <button onClick={handleAddLocation}>Add Location</button>
                <button onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default AddLocationModal;
