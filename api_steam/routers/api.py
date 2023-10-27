from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter()

data_folder = Path('../data_render')


data = {}

'''# Archivos CSV
files = ['game_genres.csv', 'genres.csv', 
         'name_games.csv', 'reviews.csv']'''



# Cargar las partes de play_time.csv y combinarlas en un solo DataFrame
play_time_parts = []
for i in range(1, 4):
    play_time_file = f'query_{i}.csv'
    play_time_path = data_folder / play_time_file
    play_time_part = pd.read_csv(play_time_path)
    play_time_parts.append(play_time_part)

play_time_combined = pd.concat(play_time_parts, ignore_index=True)

'''# Cargar otros archivos CSV
for file in files:
    file_path = data_folder / file
    data[file] = pd.read_csv(file_path)'''



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

@router.get("/anio_mas_horas2/{Genre}")
async def get_anio_mas_horas_by_genre(Genre: str):
     
     filtered_data = play_time_combined[play_time_combined['genre'] == Genre]

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
    
