// src/components/LocationModal.js
import React, { useState, useEffect } from 'react';
import './LocationModal.css';

const LocationModal = ({ isOpen, onClose }) => {
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState('');

  useEffect(() => {
    if (isOpen) {
      fetchLocations();
    }
  }, [isOpen]);

  const fetchLocations = async () => {
    // Fetch locations from backend
    const response = await fetch('/api/locations'); // Replace with your backend endpoint
    const data = await response.json();
    setLocations(data);
  };

  const handleLocationChange = (e) => {
    setSelectedLocation(e.target.value);
  };


  const handleSave = () => {
    if (selectedLocation) {
      console.log('Selected location:', selectedLocation);
    } 
    onClose();
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h2>Select or Add Location</h2>
        <div className="location-select">
          <label>
            Existing Location:
            <select value={selectedLocation} onChange={handleLocationChange}>
              <option value="">Select a location</option>
              {locations.map((location, index) => (
                <option key={index} value={location}>
                  {location}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className="location-new">
        </div>
        <div className="modal-actions">
          <button onClick={handleSave}>Save</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default LocationModal;
