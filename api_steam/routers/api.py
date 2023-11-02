from fastapi import APIRouter
import pandas as pd
from pathlib import Path
import pickle
import re
import gzip

router = APIRouter()

data_folder = Path('data_render')


data = {}

# CSV Files
files = ['playTimeGenre.csv', 'userGenre.csv',
         'usersRecommend.csv', 'usersNotRecommend.csv', 
         'sent_analysis.csv','gameRecom.csv']


# Loading files
for file in files:
    file_path = data_folder / file
    data[file] = pd.read_csv(file_path)




@router.get("/play_time_genre/{Genre}")
async def get_play_time_genre(Genre: str):
     
     '''This endpoint takes a genre as input and returns the year 
     with the most played hours for that genre from the 'playTimeGenre.csv' dataset.
     '''
     
     df = data['playTimeGenre.csv']
     
     filtered_data = df[df['genre'] == Genre]

     if not filtered_data.empty:
        
            year_with_most_hours = filtered_data['anio'].iloc[-1]

            return {
                f"Año con más horas jugadas para el Género {Genre}": int(year_with_most_hours)
            }
     else:
            return {"error": "No se encontraron datos para el género especificado"}
     


@router.get("/user_for_genre/{Genre}")
async def get_user_for_genre(Genre: str):

    '''This endpoint takes a genre as input and returns the user 
    with the most played hours for that genre and a list of hours played 
    by year from the 'userGenre.csv' dataset.
    '''

    df = data['userGenre.csv']

    result = df.groupby(['genre', 'id_user'])['playtime_forever'].sum().reset_index()
    idx = result.groupby('genre')['playtime_forever'].idxmax()
    result_max_playtime = result.loc[idx]

    user_with_max_playtime = result_max_playtime[result_max_playtime['genre'] == Genre]

    if not user_with_max_playtime.empty:
        user_id = user_with_max_playtime['id_user'].values[0]
        filtered_df = df[df['id_user'] == user_id]
        hours_played_by_year = filtered_df.groupby('year')['playtime_forever'].sum().reset_index()


        response = {
            "Usuario con más horas jugadas para " + Genre: user_id,
            "Horas jugadas": [{"Año": int(year), "Horas": int(hours/60)} for year, hours in zip(hours_played_by_year['year'], hours_played_by_year['playtime_forever'])]
        }
    else:
        response = {
            "error": "No se encontraron datos para el género especificado"
        }
    return response

    

@router.get("/top_games/{year}")
async def get_top_games(year: int):

    '''This endpoint takes a year as input and returns the top 3 most recommended games 
    by users for that year from the 'usersRecommend.csv' dataset.
    '''

    df = data['usersRecommend.csv']

   
    top_games_year = df[df['year'] == year]

    if not top_games_year.empty:
        
        top_3_games = top_games_year.nlargest(3, 'recommend_count')
        top_3_games.reset_index(drop=True, inplace=True)
        result = ["Puesto {}: {}".format(idx + 1, row['name_game']) for idx, row in top_3_games.iterrows()]
        response = {
            "Top 3 juegos para el año {}".format(year): result
        }
    else:
        response = {
            "error": "No se encontraron datos para el año especificado"
        }
    return response



@router.get("/worst_games/{year}")
async def get_worst_games(year: int):

    '''This endpoint takes a year as input and returns the top 3 least recommended games by 
    users for that year from the 'usersNotRecommend.csv' dataset.'''

    df = data['usersNotRecommend.csv']

    
    worst_games_year = df[df['year'] == year]

    if not worst_games_year.empty:
        
        worst_3_games = worst_games_year.nsmallest(3, 'recommend_count')
        worst_3_games.reset_index(drop=True, inplace=True)
        result = ["Puesto {}: {}".format(idx + 1, row['name_game']) for idx, row in worst_3_games.iterrows()]
        response = {
            "Top 3 juegos peores del año {}".format(year): result
        }
    else:
        response = {
            "error": "No se encontraron datos para el año especificado"
        }
    return response



@router.get("/sentiments_by_year")
async def sentiments_by_year(year: int):

    '''This endpoint takes a specific release year of games as input and returns 
    the count of positive, neutral, and negative sentiment categories for user reviews 
    corresponding to that year from the 'sent_analysis.csv' dataset.
    '''
    df = data['sent_analysis.csv']
    filtered_data = df[df['release year'] == year]

    sentiments = {
        "Negative": 0,
        "Neutral": 0,
        "Positive": 0
    }

    if filtered_data.empty:
        return  {
        "error": f"No se encontraron datos para el año {year}"
    }

    else:
        # Calcular la cantidad de sentimientos para el año dado
        for index, row in filtered_data.iterrows():
            sentiments[row['sentiment']] += row['recount']

        return sentiments
    

# Game Recommendation
@router.get("/recommend/")
async def get_recommendations(game_name: str):
    """
    This endpoint takes the name of a game as input and returns the top 10 recommended games 
    similar to the input game based on user playtime and genre preferences. The recommendations
    are calculated using a weighted similarity matrix.
    """

    # Cargar el DataFrame de juegos y la matriz de similitud desde archivos
    df = data['gameRecom.csv']

    file_path = Path('data_render') / 'weighted_similarity.pkl.gz'

    #with file_path.open('rb') as file:
    with gzip.open(file_path, 'rb') as file:
        weighted_similarity = pickle.load(file)

    # Normalizar el nombre del juego ingresado por el usuario
    user_game = re.sub(r'[^\w\s]', '', game_name.replace('-', ' ')).strip().upper()

    # Obtener el índice del juego ingresado por el usuario en el DataFrame
    game_index = df[df['name_game'] == user_game].index
    if len(game_index) == 0:
        return {"error": "Juego no encontrado"}
    game_index = game_index[0]

    # Calcular la similitud de coseno entre el juego del usuario y otros juegos
    similar_games = list(enumerate(weighted_similarity[game_index]))
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)
    similar_games = similar_games[1:11]  # Obtener las 10 principales recomendaciones
    game_indices = [index[0] for index in similar_games]
    recommendations = df['name_game'].iloc[game_indices].tolist()

    return {"recommendations": recommendations}

