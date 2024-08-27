// src/FilterSection.js
import React, { useState } from 'react';

function FilterSection({ filters, onFilterChange }) {
    const [localFilters, setLocalFilters] = useState(filters);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLocalFilters({ ...localFilters, [name]: value });
    };

    const applyFilters = () => {
        onFilterChange(localFilters);
    };

    return (
        <div className="filter-section">
            <input type="date" name="date_start" value={localFilters.date_start} onChange={handleChange} placeholder="Start Date" />
            <input type="date" name="date_end" value={localFilters.date_end} onChange={handleChange} placeholder="End Date" />
            <input type="time" name="time_start" value={localFilters.time_start} onChange={handleChange} placeholder="Start Time" />
            <input type="time" name="time_end" value={localFilters.time_end} onChange={handleChange} placeholder="End Time" />
            <input type="number" name="temperature_min" value={localFilters.temperature_min} onChange={handleChange} placeholder="Min Temp" />
            <input type="number" name="temperature_max" value={localFilters.temperature_max} onChange={handleChange} placeholder="Max Temp" />
            <button onClick={applyFilters}>Apply Filters</button>
        </div>
    );
}

export default FilterSection;
