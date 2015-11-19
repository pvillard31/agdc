-- new satellite: Sentinel
insert into agdc.satellite (satellite_id, satellite_name, satellite_tag, name_pattern, semi_major_axis, radius, altitude, inclination, omega, sweep_period, format, projection, spectral_filter_file, tle_format, solar_irrad_file, nominal_pixel_degrees) 
values (51, 'Sentinel 1', 'S1', NULL, 6378137, NULL, 693000, 1.7135643, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- new sensor, Sentinel 1
insert into agdc.sensor (sensor_id, satellite_id, sensor_name, description) 
values (51, 51, 'Sentinel_1', 'Sentinel 1 Radar Sensor');

-- new tile_type for Sentinel 1
-- tile type name ???
-- x/y sizes ???
-- => can the sizes be whatever we want, or do they depend on the images we get?
-- compress ???
insert into tile_type (tile_type_id, tile_type_name, crs, x_origin, y_origin, x_size, y_size, x_pixels, y_pixels, unit, file_format, file_extension, tile_directory, format_options)
values (51, 'Unprojected WGS84 10-degree at 400 pixels/degree (for SENTINEL 1 250m)', 'EPSG:4326', 0, 0, 10, 10, 4000, 4000, 'degree', 'ENVI', '.img', 'SENTINEL', 'COMPRESS=LZW');

-- no need for a new band type, sigma VV is derived
--insert into band_type (band_type_id, band_type_name) values (31, 'RBQ');

-- new band, Sigma_VV
-- file number ???
-- resolution ??? => depends on the captor/images?
-- wavelength ??? => depends on the captor? 
-- band number ???
insert into band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (510, 51, 'Sigma_VV', 4, 1, 500, 14.0850000000000009, 14.3849999999999998, null, 51, 'SigmaVV', 1);


-- new processing level for sentinel 1
-- nodata value ???
-- resampling method ???
insert into processing_level (level_id, level_name, nodata_value, resampling_method, level_description)
values (51, 'RANGE_DOPPLER_TERRAIN_CORRECTION', -28672, 'near', 'Sentinel 1 Range Doppler Terrain Correction');

-- tile layer ???
insert into band_source (tile_type_id, band_id, level_id, tile_layer) values (51, 510, 51, 10);


-- band lookup scheme
-- what is it for ???
insert into band_lookup_scheme (lookup_scheme_id, lookup_scheme_name, lookup_scheme_description)
values (51, 'Sentinel 1', 'Sentinel bands');

-- new band equivalent
-- what is it for ???
-- nominal centre, bandwidth, tolerance... ???
insert into band_equivalent (lookup_scheme_id, master_band_name, master_band_tag, nominal_centre, nominal_bandwidth, centre_tolerance, bandwidth_tolerance, band_type_id)
values (51, 'Sigma_VV', 'SigmaVV', 14.235, 0.3, 0.00025, 0.00025, 4);
