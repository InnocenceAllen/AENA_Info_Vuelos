AENA_INFOVUELOS_URL = "http://www.aena.es/csee/Satellite/infovuelos/es/"
AENA_BASE_URL = "http://www.aena.es"
DEPARTURES = "?destiny=&mov=S&origin_ac="
ARRIVALS = "?origin=&mov=L&origin_ac="
DATA_FIELDS = ['flightNumber', 'plane', 'dep_date', 'dep_time', 'dep_airport_name', 'dep_airport_code', 'dep_terminal',
               'dep_status', 'dep_weather_min', 'dep_weather_max', 'dep_weather_desc', 'dep_counter', 'dep_door',
               'arr_date', 'arr_time', 'arr_airport_name', 'arr_airport_code', 'arr_terminal', 'arr_status',
               'arr_weather_min', 'arr_weather_max', 'arr_weather_desc', 'arr_room', 'arr_belt', 'timestamp']
CSV_DELIMITER = ';'
SCRAPING_FRECUENCY = 60 #minutes