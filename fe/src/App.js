// src/App.js
import React, { useState, useEffect } from 'react';
import WeatherTable from './WeatherTable';
import './App.css';
import AddLocationModal from './AddLocationModal';
import StatusModal from './StatusModal';

function App() {
  const [data, setData] = useState([]);
  const [globeTemperatureMin, setGlobeTemperatureMin] = useState('');
  const [globeTemperatureMax, setGlobeTemperatureMax] = useState('');
  const [dateStart, setDateStart] = useState('');
  const [dateEnd, setDateEnd] = useState('');
  const [timeStart, setTimeStart] = useState('');
  const [timeEnd, setTimeEnd] = useState('');
  const [locationId, setLocationId] = useState('');
  const [temperatureMin, setTemperatureMin] = useState('');
  const [temperatureMax, setTemperatureMax] = useState('');
  const [relativeHumidityMin, setRelativeHumidityMin] = useState('');
  const [relativeHumidityMax, setRelativeHumidityMax] = useState('');
  const [showAddLocationModal, setShowAddLocationModal] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false); // Define the loading state
  const [locations, setLocations] = useState([]);
  const [page, setPage] = useState(1);  // Add page state
  const [pageSize, setPageSize] = useState(30); // Page size of 30
  const [totalPages, setTotalPages] = useState(1);


  useEffect(() => {
    // Fetch data when the component is mounted or filters change
    fetchData();
  }, [globeTemperatureMin, globeTemperatureMax, dateStart, dateEnd, timeStart, timeEnd, locationId, temperatureMin, temperatureMax, relativeHumidityMin, relativeHumidityMax, page]);

  useEffect(() => {
    // Fetch data when the component is mounted or filters change
    setPage(1)
  }, [globeTemperatureMin, globeTemperatureMax, dateStart, dateEnd, timeStart, timeEnd, locationId, temperatureMin, temperatureMax, relativeHumidityMin, relativeHumidityMax]);

  const fetchData = async () => {
    let params = new URLSearchParams();

    if (globeTemperatureMin) params.append('globe_temperature_min', globeTemperatureMin);
    if (globeTemperatureMax) params.append('globe_temperature_max', globeTemperatureMax);
    if (dateStart) params.append('date_start', dateStart);
    if (dateEnd) params.append('date_end', dateEnd);
    if (timeStart) params.append('time_start', timeStart);
    if (timeEnd) params.append('time_end', timeEnd);
    if (locationId) params.append('location_id', locationId);
    if (temperatureMin) params.append('temperature_min', temperatureMin);
    if (temperatureMax) params.append('temperature_max', temperatureMax);
    if (relativeHumidityMin) params.append('relative_humidity_min', relativeHumidityMin);
    if (relativeHumidityMax) params.append('relative_humidity_max', relativeHumidityMax);

    params.append('page', page);
    params.append('size', pageSize);

    const query = params.toString() ? `?${params.toString()}` : '';

    const response = await fetch(`http://192.168.0.114:5000/measurements/${query}`);

    const result = await response.json();
    setTotalPages(result.total); // Assuming your backend returns total pages
    setData(result.items);
  };

  const handleApplyFilter = () => {
    setPage(1); // Reset to first page
    fetchData(); // Fetch new data based on filters
  };

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1); // The `useEffect` will automatically fetch data
    }
    console.log(page)
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1); // The `useEffect` will automatically fetch data
    }
    console.log(page)
  };


  const handleExportToCSV = async () => {
    // Construct query parameters based on current filters
    let params = new URLSearchParams();

    if (globeTemperatureMin) params.append('globe_temperature_min', globeTemperatureMin);
    if (globeTemperatureMax) params.append('globe_temperature_max', globeTemperatureMax);
    if (dateStart) params.append('date_start', dateStart);
    if (dateEnd) params.append('date_end', dateEnd);
    if (timeStart) params.append('time_start', timeStart);
    if (timeEnd) params.append('time_end', timeEnd);
    if (locationId) params.append('location_id', locationId);
    if (temperatureMin) params.append('temperature_min', temperatureMin);
    if (temperatureMax) params.append('temperature_max', temperatureMax);
    if (relativeHumidityMin) params.append('relative_humidity_min', relativeHumidityMin);
    if (relativeHumidityMax) params.append('relative_humidity_max', relativeHumidityMax);

    // Construct the full export URL with query parameters
    const query = params.toString() ? `?${params.toString()}` : '';
    const exportUrl = `http://192.168.0.114:5000/measurements/export${query}`;

    // Fetch and handle the CSV export
    const response = await fetch(exportUrl);
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'weather_data.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  };


  const handleGetStatus = async () => {
    setShowStatusModal(true); // Open the modal
    setStatus(null); // Reset status
    setLoading(true); // Show loading

    try {
      const response = await fetch('http://192.168.0.114:5000/measurements/status');
      const result = await response.json();

      if (response.ok) {
        setStatus({
          status: 'Ok',
          data: result,
        });
      } else {
        setStatus({
          status: 'Error',
          data: result,
        });
      }
    } catch (error) {
      setStatus({
        status: 'Error',
        data: error.message,
      });
    } finally {
      setLoading(false); // Stop loading
    }
  };

  useEffect(() => {
    // Fetch location data
    const fetchLocations = async () => {
      try {
        const response = await fetch('http://192.168.0.114:5000/locations/');
        const result = await response.json();
        setLocations(result); // Assuming the response is an array of location objects
      } catch (error) {
        console.error("Failed to fetch locations:", error);
      }
    };

    fetchLocations();
  }, []);


  return (
    <div className="app">
      <div style={{
        display: 'flex',
        
      }}>
        <h1>sMaRT - mobile - BioMeteoS</h1>
        <button style={{ marginTop: '25px', height : '30px' }} onClick={handleGetStatus} className="status-button">Status</button>
      </div>


      <div className="filter-section">
        <div className="filter-group">
          <label>Date From</label>
          <input type="date" value={dateStart} onChange={(e) => setDateStart(e.target.value)} />
          <label>Date To</label>
          <input type="date" value={dateEnd} onChange={(e) => setDateEnd(e.target.value)} />
        </div>
        <div className="filter-group">
          <label>Time From</label>
          <input type="time" value={timeStart} onChange={(e) => setTimeStart(e.target.value)} />
          <label>Time To</label>
          <input type="time" value={timeEnd} onChange={(e) => setTimeEnd(e.target.value)} />
        </div>
        <div className="filter-group">
          <label>Temperature</label>
          <input placeholder='From' value={temperatureMin} onChange={(e) => setTemperatureMin(e.target.value)} />
          <label>Temperature</label>
          <input placeholder='To' value={temperatureMax} onChange={(e) => setTemperatureMax(e.target.value)} />
        </div>
        <div className="filter-group">
          <label>RH</label>
          <input placeholder='From' value={relativeHumidityMin} onChange={(e) => setRelativeHumidityMin(e.target.value)} />
          <label>RH</label>
          <input placeholder='To' value={relativeHumidityMax} onChange={(e) => setRelativeHumidityMax(e.target.value)} />
        </div>
        <div className="filter-group">
          <label>Globe Temperature</label>
          <input placeholder='From' value={globeTemperatureMin} onChange={(e) => setGlobeTemperatureMin(e.target.value)} />
          <label>Globe Temperature</label>
          <input placeholder='To' value={globeTemperatureMax} onChange={(e) => setGlobeTemperatureMax(e.target.value)} />
        </div>
        <div className="filter-group">
          <label>Location</label>
          <select style={{ marginTop: '5px' }} value={locationId} onChange={(e) => setLocationId(e.target.value)}>
            <option value="">Select Location</option>
            {locations.map(location => (
              <option key={location.id} value={location.id}>{location.name}</option>
            ))}
          </select>
          <button style={{ marginTop: '30px' }} className="apply-filter-button" onClick={handleApplyFilter}>Apply Filter</button>
        </div>
        <div className="filter-group">
          <button onClick={() => setShowAddLocationModal(true)}>Location</button>
          <button style={{ marginTop: '30px' }} onClick={handleExportToCSV} className="export-button">Export</button>
        </div>
        <AddLocationModal show={showAddLocationModal} onClose={() => setShowAddLocationModal(false)} />
      </div>
      <WeatherTable
        data={data}
        onNextPage={handleNextPage}
        onPreviousPage={handlePreviousPage}
        page={page} // Add this
        totalPages={totalPages} // Add this
      />
      {showStatusModal && (
        <div className="modal">
          <div className="modal-content">
            <h2>Measurement status</h2>
            {loading ? (
              <div>
                <p>Getting sensors statuses. Please wait up to 30s.</p>
                <p>Loading...</p>
              </div>

            ) : (
              <div>
                <p>Status: {status.status}</p>
                <pre>
                  {status.data && (
                    <>
                      <p>Altitude: {status.data.altitude} m</p>
                      <p>Date: {new Date(status.data.date).toLocaleDateString()}</p>
                      <p>Time: {status.data.time}</p>
                      <p>Latitude: {status.data.latitude}</p>
                      <p>Longitude: {status.data.longitude}</p>
                      <p>Globe Temperature: {status.data.globe_temperature} °C</p>
                      <p>Limited Wind Speed: {status.data.limited_wind_speed} m/s</p>
                      <p>PM 2.5: {status.data.pm_2_5} ppm</p>
                      <p>PM 10: {status.data.pm_10} ppm</p>
                      <p>UV B: {status.data.uv_b} mW/cm²</p>
                      <p>Wind Speed: {status.data.wind_speed} m/s</p>
                    </>
                  )}
                </pre>

              </div>
            )}
            <button onClick={() => setShowStatusModal(false)}>Close</button>
          </div>
        </div>
      )}
      <div className="pagination">
        <button onClick={handlePreviousPage} disabled={page <= 1}>Previous</button>
        <button onClick={handleNextPage} disabled={page >= totalPages / pageSize}>Next</button>
      </div>
    </div>
  );
}

export default App;
