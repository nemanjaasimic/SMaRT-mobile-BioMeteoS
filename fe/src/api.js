// src/api/api.js

// src/api.js
export const fetchMeasurements = async () => {
    const response = await fetch('/measurements/');
    if (!response.ok) {
      throw new Error('Failed to fetch measurements');
    }
    return await response.json();
  };
  

export const startMeasurement = async (locationId, interval) => {
    const response = await fetch('/measurements/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location_id: locationId, interval_in_s: interval })
    });
    if (!response.ok) {
        throw new Error('Failed to start measurement');
    }
    return await response.json();
};

export const stopMeasurement = async () => {
    const response = await fetch('/measurements/stop', {
        method: 'POST'
    });
    if (!response.ok) {
        throw new Error('Failed to stop measurement');
    }
    return await response.json();
};

export const fetchLocations = async () => {
    const response = await fetch('/locations');
    if (!response.ok) {
        throw new Error('Failed to fetch locations');
    }
    return await response.json();
};

export const createLocation = async (name) => {
    const response = await fetch('/locations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    if (!response.ok) {
        throw new Error('Failed to create location');
    }
    return await response.json();
};

export const checkHealthStatus = async () => {
    const response = await fetch('/measurements/status');
    if (!response.ok) {
        throw new Error('Failed to fetch health status');
    }
    return await response.json();
};
