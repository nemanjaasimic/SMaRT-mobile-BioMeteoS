// src/WeatherTable.js
import React, { useState } from 'react';
import './WeatherTable.css';
import StartMeasurementModal from './StartMeasurementModal';

function WeatherTable({ data , fetchData}) {
  const [showStartModal, setShowStartModal] = useState(false);
  const [selectedIds, setSelectedIds] = useState([]);

  // Function to handle checkbox selection
  const handleCheckboxChange = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter((itemId) => itemId !== id));
    } else {
      setSelectedIds([...selectedIds, id]);
    }
  };

  // Function to handle delete button click
  const handleDelete = async () => {
    if (selectedIds.length === 0) {
      alert('No items selected');
      return;
    }

    const confirmed = window.confirm("Are you sure you want to delete the selected items?");
    if (confirmed) {

      const response = await fetch('/api/measurements/', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ids: selectedIds }),
      });
      fetchData();

      if (!response.ok) {
        alert('Failed to delete selected items');
      }
    }
  };

  const handleStartClick = () => setShowStartModal(true);
  const handleStopClick = async () => {
    const response = await fetch('/api/measurements/stop', { method: 'POST' });
    if (response.ok) {
      alert('Measurement stopped successfully.');
    } else {
      alert('Failed to stop measurement.');
    }
  };

  return (
    <div>
      <div className="button-group">
        <button style={{marginTop: "-20px"}} className="square-button start" onClick={handleStartClick}>Start</button>
        <button style={{marginTop: "-20px"}} className="square-button stop" onClick={handleStopClick}>Stop</button>
      </div>
      <div className='weather-table-container'>
        <StartMeasurementModal show={showStartModal} onClose={() => setShowStartModal(false)} />
        <table className="weather-table">
          <thead>
            <tr>
              <th>
                <button className='delete-button' onClick={handleDelete}>Delete</button>
              </th>
              <th>Location</th>
              <th>Date</th>
              <th>Time</th>
              <th>Altitude (m)</th>
              <th>Longitude</th>
              <th>Latitude</th>
              <th>Temperature (°C)</th>
              <th>Relative Humidity (%)</th>
              <th>Globe Temp (°C)</th>
              <th>Wind Speed (m/s)</th>
              <th>Wind Speed [0.5-17](m/s)</th>
              <th>PM (2.5) ppm</th>
              <th>PM (10) ppm</th>
              <th>UV B (mW/cm^2)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.id}>
                <td>
                  <div>
                    <input type="checkbox"
                      onChange={() => handleCheckboxChange(item.id)}
                      checked={selectedIds.includes(item.id)}
                    />
                  </div>
                </td>
                <td>{item.location_name}</td>
                <td>{item.date}</td>
                <td>{item.time}</td>
                <td>{item.altitude}</td>
                <td>{item.longitude}</td>
                <td>{item.latitude}</td>
                <td>{item.temperature}</td>
                <td>{item.relative_humidity}</td>
                <td>{item.globe_temperature}</td>
                <td>{item.wind_speed}</td>
                <td>{item.limited_wind_speed}</td>
                <td>{item.pm_2_5}</td>
                <td>{item.pm_10}</td>
                <td>{item.uv_b}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default WeatherTable;
