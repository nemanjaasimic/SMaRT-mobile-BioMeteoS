import React, { useState, useEffect } from 'react';
import './StartMeasurmentModal.css';

function StartMeasurementModal({ show, onClose }) {
    const [locations, setLocations] = useState([]);
    const [selectedLocation, setSelectedLocation] = useState('');
    const [interval, setInterval] = useState(120);
    const [error, setError] = useState('');

    useEffect(() => {
        if (show) {
            fetch('http://192.168.0.114:5000/locations/')
                .then(response => response.json())
                .then(data => setLocations(data))
                .catch(() => setError('Failed to load locations.'));
        }
    }, [show]);

    const handleStartMeasurement = async () => {
        if (!selectedLocation) {
            setError('Please select a location.');
            return;
        }
        if (interval <= 0) {
            setError('Interval must be a positive number.');
            return;
        }
        
        setError(''); // Clear previous errors

        try {
            const response = await fetch('http://192.168.0.114:5000/measurements/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location_id: selectedLocation, interval_in_s: interval }),
            });

            if (response.ok) {
                alert('Measurement started successfully.');
                onClose(); // Close the modal after success
                setSelectedLocation(''); // Reset location selection
                setInterval(120); // Reset interval to default
            } else {
                throw new Error('Failed to start measurement.');
            }
        } catch (error) {
            setError(error.message);
        }
    };

    if (!show) return null;

    return (
        <div className="modal">
            <div className="modal-content">
                <h2>Start Measurement</h2>
                {error && <div className="error">{error}</div>}
                <label>
                    Select Location:
                    <select value={selectedLocation} onChange={(e) => setSelectedLocation(e.target.value)}>
                        <option value="">Select a location</option>
                        {locations.map((location) => (
                            <option key={location.id} value={location.id}>
                                {location.name}
                            </option>
                        ))}
                    </select>
                </label>
                <label>
                    Interval (in seconds):
                    <input
                        type="number"
                        value={interval}
                        onChange={(e) => setInterval(Math.max(0, e.target.value))} // Prevent negative values
                        min="1" // Ensure minimum value is 1
                    />
                </label>
                <br />
                <button className="modal-button start" onClick={handleStartMeasurement}>Start</button>
                <button className="modal-button close" onClick={onClose}>Close</button>
            </div>
        </div>
    );
}

export default StartMeasurementModal;
