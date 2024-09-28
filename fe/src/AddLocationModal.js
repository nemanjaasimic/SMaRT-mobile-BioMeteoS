import React, { useState, useEffect } from 'react';
import './AddLocationModal.css';

function AddLocationModal({ show, onClose }) {
    const [locationName, setLocationName] = useState('');
    const [locations, setLocations] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        if (show) {
            fetchLocations();
        }
    }, [show]);

    const handleAddLocation = async () => {
        const response = await fetch('/api/locations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: locationName }),
        });

        if (response.ok) {
            alert('Location added successfully.');
            setLocationName('');
            fetchLocations(); // Refresh the locations
        } else {
            alert('Failed to add location.');
        }
    };

    const fetchLocations = async () => {
        const response = await fetch('/api/locations');
        const data = await response.json();
        setLocations(data);
    };

    const handleDelete = async (locationId) => {
        try {
            const response = await fetch(`/api/locations/${locationId}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                alert('Cannot delete location with associated measurements. Delete measurements first.');
            }
            fetchLocations(); // Refresh locations after deletion
        } catch (error) {
            setErrorMessage(error.message); // Set the error message
        }
    };

    if (!show) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>Location Manager</h2>
                {errorMessage && <div className="error-message">{errorMessage}</div>}

                <label>Existing locations:</label>
                <div className="location-list">
                    <div id="locations">
                        {locations.map((location) => (
                            <div key={location.id} className="location-item">
                                <span>{location.name}</span>
                                <span 
                                    onClick={() => handleDelete(location.id)} 
                                    className="trash-icon"
                                    title="Delete location"
                                >
                                    <i className="fas fa-trash-alt" style={{ color: 'gray' }}></i>
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
                <label>New location name:</label>
                <input value={locationName} onChange={(e) => setLocationName(e.target.value)} />
                <button onClick={handleAddLocation}>Add Location</button>
                <button onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default AddLocationModal;
