-- new satellite: Percentile
insert into agdc.satellite (satellite_id, satellite_name, satellite_tag, name_pattern, semi_major_axis, radius, altitude, inclination, omega, sweep_period, format, projection, spectral_filter_file, tle_format, solar_irrad_file, nominal_pixel_degrees) 
values (53, 'Percentile', 'Percentile', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- new sensor, Moisture percentile
insert into agdc.sensor (sensor_id, satellite_id, sensor_name, description) 
values (53, 53, 'Moisture', 'Moisture percentile data');

-- new sensor, Precipitation percentile
insert into agdc.sensor (sensor_id, satellite_id, sensor_name, description) 
values (54, 53, 'Precipitation', 'Precipitation percentile data');

-- new tile_type for percentiles
insert into agdc.tile_type (tile_type_id, tile_type_name, crs, x_origin, y_origin, x_size, y_size, x_pixels, y_pixels, unit, file_format, file_extension, tile_directory, format_options)
values (53, 'Unprojected WGS84 10-degree at 4 pixels/degree (for percentiles)', 'EPSG:4326', 0, 0, 10, 10, 40, 40, 'degree', 'GTiff', '.tif', 'Percentiles', 'COMPRESS=LZW');


-- new bands
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (531, 53, 'Moisture_Percentile_65', 4, 1, 500, 14.0850000000000009, 14.3849999999999998, '.*moisture_percentile_65\..*', 53, 'Soil_moisture_percentile_65', 1);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (532, 53, 'Moisture_Percentile_75', 4, 2, 500, 14.0850000000000009, 14.3849999999999998, '.*moisture_percentile_75\..*', 53, 'Soil_moisture_percentile_75', 2);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (533, 53, 'Moisture_Percentile_85', 4, 3, 500, 14.0850000000000009, 14.3849999999999998, '.*moisture_percentile_85\..*', 53, 'Soil_moisture_percentile_85', 3);

insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (534, 54, 'Precipitation_Percentile_65', 4, 1, 500, 14.0850000000000009, 14.3849999999999998, '.*precipitation_percentile_65\..*', 53, 'Precipitation_percentile_65', 1);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (535, 54, 'Precipitation_Percentile_75', 4, 2, 500, 14.0850000000000009, 14.3849999999999998, '.*precipitation_percentile_75\..*', 53, 'Precipitation_percentile_75', 2);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (536, 54, 'Precipitation_Percentile_85', 4, 3, 500, 14.0850000000000009, 14.3849999999999998, '.*precipitation_percentile_85\..*', 53, 'Precipitation_percentile_85', 3);

-- new processing level for percentiles
insert into agdc.processing_level (level_id, level_name, nodata_value, resampling_method, level_description)
values (53, 'PERCENTILE', -32768, 'near', 'Percentiles');


-- new band source
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (53, 531, 53, 1);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (53, 532, 53, 2);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (53, 533, 53, 3);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (53, 534, 53, 1);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (53, 535, 53, 2);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (53, 536, 53, 3);