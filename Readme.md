# **STEAM MLOps - API**
Bienvenido al repositorio de STEAM MLOps - API, una aplicación desarrollada como parte de un proyecto integrador en Henry. En este proyecto, hemos implementado una API que abarca una variedad de procesos, desde la Extracción, Transformación y Carga de datos (ETL) hasta el Análisis Exploratorio de Datos (EDA) y el desarrollo de funciones con endpoints específicos.

## Características Clave

- **Procesos de ETL y EDA:** Hemos utilizado técnicas avanzadas de ETL para extraer datos de múltiples fuentes y realizar un análisis exploratorio profundo para entender mejor los datos.

- **Desarrollo de Funciones y Endpoints:** Hemos creado funciones específicas con endpoints dedicados para proporcionar funcionalidades como la búsqueda del año con más horas jugadas para un género específico, identificar el usuario con más horas jugadas para un género dado, y ofrecer recomendaciones de juegos basadas en un sistema de recomendación mediante la similitud de coseno.

- **Sistema de Recomendación Avanzado:** Implementamos un sistema de recomendación basado en la similitud de coseno, utilizando técnicas avanzadas de aprendizaje automático para proporcionar a los usuarios recomendaciones precisas y personalizadas.

- **Despliegue en Render:** La API está alojada en un servicio web de [Render_STEAM](https://steammlops-api.onrender.com/docs#/), asegurando una experiencia de usuario eficiente y confiable.

## Objetivos del Proyecto
### 1. PlayTimeGenre
Esta función debe devolver el año con más horas jugadas para un género dado.
Ejemplo de retorno:
```json
{"Año de lanzamiento con más horas jugadas para Género X": 2013}
```

### 2. UserForGenre
Esta función debe devolver el usuario que acumula más horas jugadas para el género dado, junto con una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno:
```json
{
  "Usuario con más horas jugadas para Género X": "us213ndjss09sdf",
  "Horas jugadas": [
    {"Año": 2013, "Horas": 203},
    {"Año": 2012, "Horas": 100},
    {"Año": 2011, "Horas": 23}
  ]
}
```
### 3. UsersRecommend
Esta función debe devolver el top 3 de juegos MÁS recomendados por usuarios para un año dado (reviews.recommend = True y comentarios positivos/neutrales).
Ejemplo de retorno:
```json
[
  {"Puesto 1": "X"},
  {"Puesto 2": "Y"},
  {"Puesto 3": "Z"}
]
```
### 4. UsersNotRecommend
Esta función debe devolver el top 3 de juegos MENOS recomendados por usuarios para un año dado (reviews.recommend = False y comentarios negativos).
Ejemplo de retorno:
```json
[
  {"Puesto 1": "X"},
  {"Puesto 2": "Y"},
  {"Puesto 3": "Z"}
]
```
### 5. Sentiment_Analysis
Esta función debe devolver una lista con la cantidad de registros de reseñas de usuarios categorizados con un análisis de sentimiento según el año de lanzamiento del juego.
Ejemplo de retorno:
```json
{"Negative": 182, "Neutral": 120, "Positive": 278}
```
### 6. Sistema de Recomendación Item-Item
Implementación de un modelo de aprendizaje automático para recomendar juegos similares.
Ejemplo de retorno:
```json
{
  "recommendations": [
    "TOTAL WARTM ROME II   EMPEROR EDITION",
    "XCOM ENEMY UNKNOWN",
    "AGE OF EMPIRES II HD",
    "COMPANY OF HEROES 2",
    "EMPIRE TOTAL WARTM"
  ]
}
```

## Desarrollo del Proyecto

1. Se estudió la información del archivo [data_dictionary.xlsx](https://github.com/leocorbur/SteamMLOps-API/blob/main/data_dictionary.xlsx) y se extrajo la información de los archivos almacenados en la carpeta 'raw_data', los cuales estaban en formatos .json y comprimidos .gz.
2. Los 3 archivos contenían información sobre nombres de juegos, fechas de lanzamiento, comentarios de usuarios y tiempo de juego (minutos) por usuario por juego.
3. En el notebook [elt_eda_steam.ipynb](https://github.com/leocorbur/SteamMLOps-API/blob/main/etl_eda_steam.ipynb), se realizó el ETL utilizando el método *ast.literal_eval()* para la extracción de registros y se aplicaron transformaciones y limpieza de datos, junto con un EDA para seleccionar las columnas necesarias para las funciones solicitadas.
4. El resultado del notebook fue la obtención de 5 datasets ubicados en la carpeta [datasets](https://github.com/leocorbur/SteamMLOps-API/tree/main/datasets), con reducción de tamaño en comparación con la data original.
5. Se creó la carpeta [api_steam](https://github.com/leocorbur/SteamMLOps-API/tree/main/api_steam) y su respectivo entorno virtual, con las librerías y dependencias necesarias especificadas en 'requirements.txt'. Para el desarrollo de los endpoints, se utilizó el framework FastAPI junto con Pandas, Numpy y otras bibliotecas.
6. Se realizaron uniones y transformaciones de datasets en los notebooks [mergeDatasets.ipynb](https://github.com/leocorbur/SteamMLOps-API/blob/main/api_steam/mergeDatasets.ipynb) y [MLOps_steam](https://github.com/leocorbur/SteamMLOps-API/blob/main/MLOps_steam.ipynb) para preparar los datos para las funciones específicas.
7. Se comprobó el funcionamiento de las funciones utilizando la dependencia uvicorn main:app en el localhost.
8. Finalmente, se subió el código al repositorio en GitHub y se asoció con Render para el despliegue del MVP.


## Contribuyentes

- **Leonel Cortez**
  - GitHub: [leocorbur](https://github.com/leocorbur)
  - Correo electrónico: leocorbur@gmail.com
  - Rol: Desarrollador principal

## Agradecimientos 

Agradecemos a Henry por proporcionar la oportunidad de trabajar en este proyecto y a todos los contribuyentes que participaron en el desarrollo.

Para obtener más detalles sobre el desarrollo del proyecto y cómo utilizar las funciones, consulte la documentación detallada en los archivos correspondientes del repositorio. ¡Gracias por su interés en STEAM MLOps - API!