
# AENA Flights
> Información sobre vuelos en los aeropuertos españoles

![alt text](https://goo.gl/QpQcAF)

# Contexto

Viajar es una de las actividades preferidas de las personas. Sin importar el motivo, anualmente más de 3 mil millones de personas visitan diferentes destinos (Cantidad de viajeros). En el caso de los españoles, no solo seleccionan placeres internacionales. Según el Instituto Nacional de Estadística, en el año 2017, 6.298.419 españoles visitaron lares foráneos. Sin embargo, 57.693.025 locales, ya sea por motivos de trabajo o placer, se trasladaron dentro del país y de estos, más de 2 millones mediante el tercer medio más utilizado en España para estos fines, el transporte aéreo (Libro INE).

Cada aerolínea tiene su propia web, donde los clientes pueden comprar billetes, realizar la facturación, y obtener información actualizada sobre el estado de sus vuelos.

Además, han surgido diferentes webs dedicadas a ofrecer servicios relacionados con el transporte aéreo. La mayoría se orientan a la búsqueda de vuelos y comparación de precios para encontrar la más barata, son los llamados metabuscadores, como [Kayak](https://www.kayak.com) o [Skyscanner](https://www.skyscanner.es/).  

También han surgido algunas Webs especializadas en ofrecer información en tiempo real sobre vuelos y aeropuertos, siendo [FlightStats](https://www.flightstats.com) una de las más conocidas. 

Todas estas webs son servicios de agregación, pues  obtienen y combinan en un único punto de acceso, datos procedentes de distintas fuentes, con el fin de ofrecer un valor añadido al usuario (encontrar el vuelo más barato en el primer caso, ofrecer información adicional o presentarla en un formato más atractivo o útil).

La gestión de los aeropuertos y el tráfico aéreo en España recae en la empresa Aena SA y Aena Aeropuertos, una empresa a medio camino entre los público y lo privado. En este proyecto nos planteamos obtener, mediante técnicas de *scraping*, información sobre los vuelos que con origen o destino en los aeropuertos españoles, la cual se puede obtener de la Web de dicha empresa
[(https://www.aena.es)](https://www.aena.es). En particular, desde el apartado denominado Infovuelos es posible obtener información sobre los vuelos que llegan o despegan de cualquier aeropuerto en territorio español. Una recopilación sistemática de esta información permitiría realizar análisis a posteriori con los cuales podríamos responder preguntas interesantes, tal y como describimos más adelante, en la sección Inspiración.

## Contenido

La información capturada contiene los detalles de todos los vuelos que discurren por los aeropuertos españoles en un momento dado. Los detalles de cada vuelo incluyen la información más elemental, como el número de vuelo, la fecha y la hora, y los aeropuertos de origen y destino. Pero además, se incluyen otros atributos a priori menos interesantes pero con potencial para realizar tareas de minería de datos a posteriori, como el modelo de avión o las previsiones climáticas para los lugares de origen y destino.

En total, para caracterizar cada vuelo hemos encontrado un total de 24 atributos, aunque no siempre están presentes, sobre todo cuando se trata de aeropuertos internacionales.:

| Campo | Descripción | Tipo de dato | Muestra |
| ----- | ----------- | ---- | ------- |
| flightNumber | Número de vuelo | String |	AEA7232 |
| plane | Nombre del avión | String	| ATR-72 |
| dep_date | Fecha de salida | Datetime	|13/04/18
| dep_time | Hora de salida | Datetime	| 06:30
| dep_airport_name | Nombre del aeropuerto de salida |String|	A Coruña|
| dep_airport_code | Código del aeropuerto de salida |String|	LCG|
| dep_terminal | Terminal de salida | Integer|	1|
| dep_status | Estado de la salida | String|	Salida prevista a las 07:00|
| dep_weather_min | Temperatura mínima de salida | Integer|	10|
| dep_weather_max | Temperatura máxima de salida |Integer|	15|
| dep_weather_desc | Descripción del clima de salida |String|	Nubosidad variable|
| dep_counter | Mostrador de salida |Integer|	6|
| dep_door | Puerta de salida |Integer|	7|
| arr_date | Fecha de arribo |Datetime	|13/04/18|
| arr_time | Hora de arribo |Datetime|	08:40|
| arr_airport_name | Nombre del aeropuerto de arribo |String|	Barcelona-El Prat|
| arr_terminal | Terminal de llegada |String|	T1|
| arr_status | Estado del llegada |String|	Llegada prevista a las 08:40|
| arr_weather_min | Temperatura mínima de llegada |Integer|	12|
| arr_weather_max | Temperatura máxima de llegada |Integer|	17|
| arr_weather_desc | Descripción del clima de llegada |String |	Lluvia débil|
| arr_room | Cuarto de llegada | String |	T1_G |
| arr_belt | Zona de llegada |Integer |	7 |
| timestamp | Marca de tiempo | Datetime | 2018-04-12 23:42:0 8|

Con el propósito de recoger la información lo más completa posible se realizó el web scrapping cada 3 horas durante 3 días consecutivos, recopilando un total de 200kb. El código encargado de realizar esta operación fue desarrollado en Python 3.5 con la ayuda de la libreríaBeautifulSoup4. El período de tiempo de los datos es de 11/4/2018 hasta el 13/4/2018 y se obtuvieron un total de 2563 observaciones.

## Agradecimientos


## Inspiración
 Conocer qué tanto afecta el clima en las salidas de los vuelos, qué vuelos se retrasan mayormente o con menor frecuencia; los aeropuertos que presentan más vuelos y las horas picos de estos, forman parte de la información a extraer que hace llamativo el conjunto de datos.
 ¿Qué ciudades son las preferidas por los ciudadanos?¿Qué vuelos son más eficientes respecto al tiempo? ¿Qué tan lleno estará el aeropuerto a la hora de buscar a mis familiares?¿Qué clima puede perjudicar mi vuelo? Estas pueden ser algunas de las preguntas de la comunidad que pueden ser respuestas mediante el análisis de este conjunto de datos.
 El rendimiento de las aerolíneas puede salir a relucir, lo que ha de permitir a las personas realizar mejores decisiones en la selección de vuelos. A su vez, podrán organizarse de mejor manera y con antelación.

## Licencia
Se liberará el material bajo la licencia Attribution-NonComercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) con la principal intención de compartir y permitir el uso de esta información de manera razonable mientras no sea con fines comerciales.
Esta licencia da la libertad de compartir y adaptar el material mientras se de el crédito apropiado a los autores, se use el material con fines no comerciales y en caso de que se realicen transformaciones, las distribuciones se realicen bajo la misma licencia.
>https://creativecommons.org/licenses/by-nc-sa/4.0/
