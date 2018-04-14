![alt text](https://goo.gl/QpQcAF)
# AENA Flights
> Información sobre vuelos en los aeropuertos españoles

# Contexto
La información capturada contiene los detalles de todos los vuelos que ocurren en cada aeropuerto del país en determinado día. El conjunto de datos recopila datos referentes a los factores que caracterizan o influyen en determinado vuelo en el momento de salida y llegada a su destino.
# Contenido
Para caracterizar cada vuelo se utilizan 24 variables descritas a continuación:
| Campo | Descripción | Tipo | Muestra |
| ----- | ----------- | ---- | ------- |
| flightNumber | Número de vuelo |
| plane | Nombre del avión |
| dep_date | Fecha de salida |
| dep_time | Hora de salida |
| dep_airport_name | Nombre del aeropuerto de salida |
| dep_airport_code | Código del aeropuerto de salida |
| dep_terminal | Terminal de salida |
| dep_status | Estado de la salida |
| dep_weather_min | Temperatura mínima de salida |
| dep_weather_max | Temperatura máxima de salida |
| dep_weather_desc | Descripción del clima de salida |
| dep_counter | Mostrador de salida |
| dep_door | Puerta de salida |
| arr_date | Fecha de arribo |
| arr_time | Hora de arribo |
| arr_airport_name | Nombre del aeropuerto de arribo |
| arr_terminal | Terminal de llegada |
| arr_status | Estado del llegada |
| arr_weather_min | Temperatura mínima de llegada |
| arr_weather_max | Temperatura máxima de llegada |
| arr_weather_desc | Descripción del clima de llegada |
| arr_room | Cuarto de llegada |
| arr_belt | Zona de llegada |
| timestamp | Marca de tiempo |

Con el propósito de recoger la información lo más completa posible se realizó el web scrapping cada 3 horas durante 3 días consecutivos. El código encargado de realizar esta operación fue desarrollado en Python 3.5 con la ayuda de la libreríaBeautifulSoup4. El período de tiempo de los datos es de (FECHA)
# Agradecimientos
El conjunto de datos es obtenido del sitio web de Aena, SA y Aena Aeropuertos (www.aena.es), una empresa dedicada a gestionar los vuelos de los aeropuertos españoles.
# Inspiración
 Conocer qué tanto afecta el clima en las salidas de los vuelos, qué vuelos se retrasan mayormente o con menor frecuencia; los aeropuertos que presentan más vuelos y las horas picos de estos, forman parte de la información a extraer que hace llamativo el conjunto de datos.
 ¿Qué ciudades son las preferidas por los ciudadanos?¿Qué vuelos son más eficientes respecto al tiempo? ¿Qué tan lleno estará el aeropuerto a la hora de buscar a mis familiares?¿Qué clima puede perjudicar mi vuelo? Estas pueden ser algunas de las preguntas de la comunidad que pueden ser respuestas mediante el análisis de este conjunto de datos. .

# Licencia
Se liberará el material bajo la licencia Attribution-NonComercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) con la principal intención de compartir y permitir el uso de esta información de manera razonable mientras no sea con fines comerciales.
Esta licencia da la libertad de compartir y adaptar el material mientras se de el crédito apropiado a los autores, se use el material con fines no comerciales y en caso de que se realicen transformaciones, las distribuciones se realicen bajo la misma licencia.


