import sys
import warnings
sys.path.append("../ass-01")
import math
import ass01

def get_single_prediction(userA, ratings, movie, movies, top10usr, dict):
    prd = ass01.prediction(userA, top10usr, movie, ratings) #calculate prediction on a specific movie
    if not math.isnan(prd):
        dict.update({movies[movies['movieId'] == movie].iloc[0]['movieId'] : prd}) #add the film title and the prediction to the dict

def get_all_predictions(userA, ratings, movies, column, top10usr, dict):
    movies[column].map(lambda x: get_single_prediction(userA, ratings, x, movies, top10usr, dict))

def get_predicted_mvs(input_users, ratings, movies): #function that gets 10 predicted movies for every user in input (from ass01)
    pred_movies = dict()
    similar_users = dict()
    df_users = ass01.get_all_users(ratings)
    for user in input_users:
        user_ratings = ass01.get_usr_rows(ratings, 'userId', user)
        topusers = dict()
        ass01.get_all_similarities(user, user_ratings, ratings, df_users, topusers) #get the similarity on every user of df
        top10usr = ass01.get_top10(topusers) #get top 10 users similar to user in input
        similar_users[user] = top10usr #save most similar users to user in input 

        user_films = ass01.get_column(user_ratings, 'movieId') #get movies rated by user
        mvs = ass01.get_df_difference(movies, user_films) #get movies not rated by user
        mvs_sugg = dict() #movies to sugget to user in input
        get_all_predictions(user, ratings, mvs, 'movieId', top10usr, mvs_sugg) #get the prediction on every movie not rated by user
        top10mvs = ass01.get_top10(mvs_sugg) #get top 10 films to suggest to user in input
        
        for movie in top10mvs.keys():
            rate = top10mvs.get(movie) #get the rate of the movie suggested for user in input
            if movie in pred_movies.keys(): #check if the movie is already in the output dictionary
                pred_movies[movie][user] = rate #add couple (user, rate) for that movie
            else:
                pred_movies[movie] = {user : rate} #first couple, add it for that movie

    return (pred_movies, similar_users)

def avg_method(users, pred_movies, similar_users, ratings):
    avg = 0
    for movie in pred_movies.keys():
        for user in users:
            pred = 0
            try:
                pred = pred_movies[movie][user] #try if this movie has already been predicted for user in input
            except:
                user_ratings = ass01.get_usr_rows(ratings, 'userId', user) #get user's ratings
                mvs_rated = ass01.get_column(user_ratings, 'movieId') #get movies rated by user in input
                if movie in set(mvs_rated): #if user has already watched the movie
                    pred = user_ratings[user_ratings['movieId'] == movie].iloc[0]['rating'] #get its rate 
                else:
                    pred = ass01.prediction(user, similar_users[user], movie, ratings) #unless, get its rate prediction
                
                pred_movies[movie][user] = pred #update the score of the user in input for the movie

            if not math.isnan(pred):
                avg += pred
        
        avg = avg/len(users) #get the mean of the scores as the group score
        pred_movies[movie] = avg #update the group score for the movie as average method

    return pred_movies

def least_misery_method(users, pred_movies, similar_users, ratings):
    for movie in pred_movies.keys():
        for user in users:
            try:
                pred_movies[movie][user] #try if this movie has already been predicted for user in input
            except:
                pred = 0
                user_ratings = ass01.get_usr_rows(ratings, 'userId', user) #get user ratings
                mvs_rated = ass01.get_column(user_ratings, 'movieId') #et movies rated by user in input
                if movie in set(mvs_rated): #if user has already watched the movie
                    pred = user_ratings[user_ratings['movieId'] == movie].iloc[0]['rating'] #get its rate 
                else:
                    pred = ass01.prediction(user, similar_users[user], movie, ratings) #unless, get its rate prediction

                if not math.isnan(pred):
                    pred_movies[movie][user] = pred #update the score of the user in input for the movie
            
        pred_movies[movie] = min(dict(pred_movies[movie]).values()) #update the group score for the movie as least misery method

    return pred_movies    