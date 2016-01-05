-- new satellite: Sentinel
insert into agdc.satellite (satellite_id, satellite_name, satellite_tag, name_pattern, semi_major_axis, radius, altitude, inclination, omega, sweep_period, format, projection, spectral_filter_file, tle_format, solar_irrad_file, nominal_pixel_degrees) 
values (51, 'Sentinel 1', 'S1', NULL, 6378137, NULL, 693000, 1.7135643, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- new sensor, Sentinel 1
insert into agdc.sensor (sensor_id, satellite_id, sensor_name, description) 
values (51, 51, 'Sentinel_1', 'Sentinel 1 Radar Sensor');

-- new tile_type for Sentinel 1
-- tile type name ???
insert into tile_type (tile_type_id, tile_type_name, crs, x_origin, y_origin, x_size, y_size, x_pixels, y_pixels, unit, file_format, file_extension, tile_directory, format_options)
values (51, 'Unprojected WGS84 1-degree at 4000 pixels/degree (for SENTINEL 1)', 'EPSG:4326', 0, 0, 1, 1, 4000, 4000, 'degree', 'GTiff', '.tif', 'SENTINEL', 'COMPRESS=LZW');

-- no need for a new band type, sigma VV is derived
--insert into band_type (band_type_id, band_type_name) values (31, 'RBQ');

-- new band, Sigma_VV
-- resolution ??? => depends on the captor/images?
-- wavelength ??? => depends on the captor? 
insert into band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (510, 51, 'Sigma_VV', 4, 1, 500, 14.0850000000000009, 14.3849999999999998, null, 51, 'SigmaVV', 1);


-- new processing level for sentinel 1
-- resampling method ???
insert into processing_level (level_id, level_name, nodata_value, resampling_method, level_description)
values (51, 'RANGE_DOPPLER_TERRAIN_CORRECTION', -28672, 'near', 'Sentinel 1 Range Doppler Terrain Correction');

-- new band source
insert into band_source (tile_type_id, band_id, level_id, tile_layer) values (51, 510, 51, 1);

