-- new satellite: Forecast
insert into agdc.satellite (satellite_id, satellite_name, satellite_tag, name_pattern, semi_major_axis, radius, altitude, inclination, omega, sweep_period, format, projection, spectral_filter_file, tle_format, solar_irrad_file, nominal_pixel_degrees) 
values (54, 'Forecast', 'Forecast', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- new sensor, Total precipitation
insert into agdc.sensor (sensor_id, satellite_id, sensor_name, description) 
values (55, 54, 'Total_precipitation', 'Total precipitation forecast');

-- new tile_type for Forecast
insert into agdc.tile_type (tile_type_id, tile_type_name, crs, x_origin, y_origin, x_size, y_size, x_pixels, y_pixels, unit, file_format, file_extension, tile_directory, format_options)
values (54, 'Unprojected WGS84 10-degree at 4 pixels/degree (for forecast)', 'EPSG:4326', 0, 0, 10, 10, 40, 40, 'degree', 'GTiff', '.tif', 'Forecast', 'COMPRESS=LZW');


-- new bands
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (540, 55, 'Total_precipitation_24h', 4, 1, 500, 14.0850000000000009, 14.3849999999999998, '.*f024_total_precipitation\.tif', 54, 'Total_precipitation_24h', 1);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (541, 55, 'Total_precipitation_30h', 4, 2, 500, 14.0850000000000009, 14.3849999999999998, '.*f030_total_precipitation\.tif', 54, 'Total_precipitation_30h', 2);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (542, 55, 'Total_precipitation_72h', 4, 3, 500, 14.0850000000000009, 14.3849999999999998, '.*f072_total_precipitation\.tif', 54, 'Total_precipitation_72h', 3);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (543, 55, 'Total_precipitation_78h', 4, 4, 500, 14.0850000000000009, 14.3849999999999998, '.*f078_total_precipitation\.tif', 54, 'Total_precipitation_78h', 4);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (544, 55, 'Total_precipitation_120h', 4, 5, 500, 14.0850000000000009, 14.3849999999999998, '.*f120_total_precipitation\.tif', 54, 'Total_precipitation_120h', 5);
insert into agdc.band (band_id, sensor_id, band_name, band_type_id, file_number, resolution, min_wavelength, max_wavelength, file_pattern, satellite_id, band_tag, band_number)
values (545, 55, 'Total_precipitation_126h', 4, 6, 500, 14.0850000000000009, 14.3849999999999998, '.*f126_total_precipitation\.tif', 54, 'Total_precipitation_126h', 6);


-- new processing level for Forecast
insert into agdc.processing_level (level_id, level_name, nodata_value, resampling_method, level_description)
values (55, 'TOTAL_PRECIPITATION_FORECAST', -32768, 'near', 'Total Precipitation Forecast');


-- new band source
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (54, 540, 55, 1);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (54, 541, 55, 2);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (54, 542, 55, 3);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (54, 543, 55, 4);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (54, 544, 55, 5);
insert into agdc.band_source (tile_type_id, band_id, level_id, tile_layer) values (54, 545, 55, 6);