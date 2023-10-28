from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter()

data_folder = Path('data_render')


data = {}

# Archivos CSV
files = ['playTimeGenre.csv', 'userGenre.csv','usersRecommend.csv', 'usersNotRecommend.csv']



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

# PlayTimeGenre( genero : str ): Debe devolver año con mas horas jugadas para dicho género.

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
     

     
#UserForGenre( genero : str ): Debe devolver el usuario que acumula más horas jugadas 
#para el género dado y una lista de la acumulación de horas jugadas por año.

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

    
# UsersRecommend( año : int ): Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado

@router.get("/top_games/{year}")
async def get_top_games(year: int):

    # Agrupa por id_game y cuenta las recomendaciones para cada juego en el año dado
    top_games = data['usersRecommend.csv'].groupby(['name_game', 'year']).size().reset_index(name='recommend_count')

    # Filtra los juegos para el año dado
    top_games_year = top_games[top_games['year'] == year]

    if not top_games_year.empty:
        # Ordena los juegos por la cantidad de recomendaciones en orden descendente y toma los primeros 3
        top_3_games = top_games_year.nlargest(3, 'recommend_count')
        top_3_games.reset_index(drop=True, inplace=True)

        # Formatea el resultado en la estructura deseada
        result = [{"Puesto {}: {}".format(idx + 1, row['name_game'])} for idx, row in top_3_games.iterrows()]
        response = {
            "Top 3 juegos para el año {}".format(year): result
        }
    else:
        response = {
            "error": "No se encontraron datos para el año especificado"
        }
    return response

# UsersNotRecommend( año : int ): Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado

@router.get("/worst_games/{year}")
async def get_worst_games(year: int):


    # Filtra los juegos para el año dado
    worst_games_year = data['usersNotRecommend.csv'][data['usersNotRecommend.csv']['year'] == year]

    if not worst_games_year.empty:
        # Ordena los juegos por la cantidad de recomendaciones en orden descendente y toma los primeros 3
        worst_3_games = worst_games_year.nsmallest(3, 'recommend_count')
        worst_3_games.reset_index(drop=True, inplace=True)

        # Formatea el resultado en la estructura deseada
        result = [{"Puesto {}: {}".format(idx + 1, row['name_game'])} for idx, row in worst_3_games.iterrows()]
        response = {
            "Top 3 juegos peores del año {}".format(year): result
        }
    else:
        response = {
            "error": "No se encontraron datos para el año especificado"
        }
    return response

