-- new satellite: SMOS
insert into agdc.satellite (satellite_id, satellite_name, satellite_tag, name_pattern, semi_major_axis, radius, altitude, inclination, omega, sweep_period, format, projection, spectral_filter_file, tle_format, solar_irrad_file, nominal_pixel_degrees) 
values (52, 'SMOS', 'SMOS', NULL, 7137456.50, NULL, NULL, 1.710422667, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- new sensor, Sentinel 1
insert into agdc.sensor (sensor_id, satellite_id, sensor_name, description) 
values (52, 52, 'SMOS', 'SMOS Sensor');


-- new tile_type for Sentinel 1
-- tile type name ???
insert into agdc.tile_type (tile_type_id, tile_type_name, crs, x_origin, y_origin, x_size, y_size, x_pixels, y_pixels, unit, file_format, file_extension, tile_directory, format_options)
values (52, 'Unprojected WGS84 10-degree at 4 pixels/degree (for SMOS)', 'EPSG:4326', 0, 0, 10, 10, 40, 40, 'degree', 'GTiff', '.tif', 'SMOS', 'COMPRESS=LZW');

-- no need for a new band type, sigma VV is derived
--insert into band_type (band_type_id, band_type_name) values (31, 'RBQ');

-- new bands
-- resolution ??? => depends on the captor/images?
-- wavelength ??? => depends on the captor? 
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (520, 52, 'Soil_Moisture', 4, 1, 500, 14.0850000000000009, 14.3849999999999998, '.*Soil_Moisture\..*', 52, 'Soil_Moisture', 1);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (521, 52, 'Soil_Moisture_Dqx', 4, 2, 500, 14.0850000000000009, 14.3849999999999998, '.*Soil_Moisture_Dqx\..*', 52, 'Soil_Moisture_Dqx', 2);

-- new processing level for sentinel 1
-- resampling method ???
insert into agdc.processing_level (level_id, level_name, nodata_value, resampling_method, level_description)
values (52, 'MOISTURE', -32768, 'near', 'SMOS Soil Moisture');

-- new band source
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (52, 520, 52, 1);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (52, 521, 52, 2);
