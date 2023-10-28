from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter()

data_folder = Path('data_render')


data = {}

# Archivos CSV
files = ['playTimeGenre.csv', 'userGenre.csv']



'''file_path = data_folder/'query_1.csv'
play_time_combined = pd.read_csv(file_path)'''

# Cargar archivos CSV
for file in files:
    file_path = data_folder / file
    data[file] = pd.read_csv(file_path)



'''
# Ruta para obtener el anio con mas horas jugadas del id_genre 
@router.get("/anio_mas_horas/{id_genre}")
async def get_anio_mas_horas_by_id(id_genre: int):

    # Realizar unión de datos de play_time.csv y game_genres.csv basada en 'id_game'
    merged_data = pd.merge(data['play_time.csv'], data['game_genres.csv'], on='id_game', how='left')
    merged_data = pd.merge(merged_data, data['name_games.csv'], on='id_game', how='left')
        
    # Filtrar por el 'game_id' específico
    filtered_data = merged_data[merged_data['id_genre'] == id_genre]

    if not filtered_data.empty:
            # Calcular las horas totales jugadas por año
            hours_by_year = filtered_data.groupby(filtered_data['anio'])['playtime_forever'].sum()

            # Encontrar el año con más horas jugadas
            year_with_most_hours = hours_by_year.idxmax()

            return {
                "Año con más horas jugadas para Género": year_with_most_hours
            }
    else:
            return {"error": "No se encontraron datos para el género especificado"}
'''
    

'''# Ruta para obtener el anio con mas horas jugadas de un genre 
@router.get("/anio_mas_horas/{Genre}")
async def get_anio_mas_horas_by_genre(Genre: str):

    # Realizar unión de datos de play_time.csv y game_genres.csv basada en 'id_game'
    merged_data = pd.merge(play_time_combined, data['game_genres.csv'], on='id_game', how='left')
    merged_data = pd.merge(merged_data, data['name_games.csv'], on='id_game', how='left')
    merged_data = pd.merge(merged_data, data['genres.csv'], on='id_genre', how='left')
        
    # Filtrar por el 'game_id' específico
    filtered_data = merged_data[merged_data['genre'] == Genre]

    if not filtered_data.empty:
            # Calcular las horas totales jugadas por año
            hours_by_year = filtered_data.groupby(filtered_data['anio'])['playtime_forever'].sum()

            # Encontrar el año con más horas jugadas
            year_with_most_hours = hours_by_year.idxmax()

            return {
                f"Año con más horas jugadas para el Género {Genre}": year_with_most_hours
            }
    else:
            return {"error": "No se encontraron datos para el género especificado"}
    '''

# 01.1 Ruta para obtener el anio con mas horas jugadas de un genre 

@router.get("/anio_mas_horas/{Genre}")
async def get_anio_mas_horas_by_genre(Genre: str):
     
     filtered_data = data['playTimeGenre.csv'][data['playTimeGenre.csv']['genre'] == Genre]

     if not filtered_data.empty:
            # Calcular las horas totales jugadas por año
            hours_by_year = filtered_data.groupby(filtered_data['anio'])['playtime_forever'].sum()

            # Encontrar el año con más horas jugadas
            year_with_most_hours = hours_by_year.idxmax()

            return {
                f"Año con más horas jugadas para el Género {Genre}": int(year_with_most_hours)
            }
     else:
            return {"error": "No se encontraron datos para el género especificado"}
     
@router.get("/user_for_genre/{Genre}")
async def get_user_for_genre(Genre: str):


    result = data['userGenre.csv'].groupby(['genre', 'id_user'])['playtime_forever'].sum().reset_index()
    idx = result.groupby('genre')['playtime_forever'].idxmax()
    result_max_playtime = result.loc[idx]

    # Obtener el usuario con más horas jugadas para el género dado
    user_with_max_playtime = result_max_playtime[result_max_playtime['genre'] == Genre]

    if not user_with_max_playtime.empty:
        user_id = user_with_max_playtime['id_user'].values[0]
        filtered_df = data['userGenre.csv'][data['userGenre.csv']['id_user'] == user_id]
        # Agrupar por año y sumar las horas jugadas
        hours_played_by_year = filtered_df.groupby('year')['playtime_forever'].sum().reset_index()

        # Crear el diccionario de retorno
        response = {
            "Usuario con más horas jugadas para " + Genre: user_id,
            "Horas jugadas": [{"Año": int(year), "Horas": int(hours/60)} for year, hours in zip(hours_played_by_year['year'], hours_played_by_year['playtime_forever'])]
        }
    else:
        response = {
            "error": "No se encontraron datos para el género especificado"
        }
    return response
    
