import pandas as pd
import numpy as np
import math

def read(file_path1, file_path2):
    ratings = pd.read_csv(file_path1).drop('timestamp', axis = 1) #open csv file and drop 'timestamp' column, it is not necessary
    movies = pd.read_csv(file_path2).drop(['genres'], axis = 1) #open csv file and drop 'timestamp'  and 'genres' columns, they are not necessary

    return (ratings, movies)

def get_all_users(df):
    return df.groupby('userId').groups.keys() #all the users of the dataset

def get_usr_rows(df, column, user):
    return df[df[column] == user]

def get_column(df, column):
    return df[column]

def get_df_difference(df1, df2):
    return pd.concat([df1, df2]).drop_duplicates(keep=False)

def jaccard_similarity(df_user1, df_user2): #Jaccard similarity function for computing similarities between users
    merged_ratings = df_user1.merge(df_user2, on = "movieId", how = "inner") #number of ratings of movies in common
    same_rates = len(set(merged_ratings['rating_x']) & set(merged_ratings['rating_y'])) #number of same rates on the same movies
    if merged_ratings.empty == True or same_rates == 0:
        return math.nan

    try:
        jac = len(same_rates)/len(merged_ratings)
    except (RuntimeWarning, ZeroDivisionError):
        return math.nan

    return jac

def euclidean_distance_similarity(df_user1, df_user2):
    merged_ratings = df_user1.merge(df_user2, on = "movieId", how = "inner") #merged df with movies rated by both users
    if merged_ratings.empty == True:
        return math.nan
    
    ratings_user1 = merged_ratings['rating_x']
    ratings_user2 = merged_ratings['rating_y']
    dis = np.sqrt((np.sum((ratings_user1 - ratings_user2)**2))) #calculate euclidean distance

    return 1/(1 + dis) #return normalization between 0 and 1

def cosine_similarity(df_user1, df_user2): #Cosine similarity function for computing similarities between users
    merged_ratings = df_user1.merge(df_user2, on = "movieId", how = "inner") #merged df with movies rated by both users
    if merged_ratings.empty == True:
        return math.nan
    
    ratings_user1 = merged_ratings['rating_x'] #vector of ratings of user1
    ratings_user2 = merged_ratings['rating_y'] #vector of ratings of user2
    
    num = np.sum((ratings_user1 * ratings_user2))
    den = np.sqrt(np.sum((ratings_user1**2))) * np.sqrt(np.sum((ratings_user2**2)))

    try:
        cos = num/den
    except (RuntimeWarning, ZeroDivisionError):
        return math.nan
    
    return cos

def pearson_correlation(df_user1, df_user2): #Pearson correlation function for computing similarities between users
    merged_ratings = df_user1.merge(df_user2, on = "movieId", how = "inner") #merged df with movies rated by both users
    if merged_ratings.empty == True:
        return math.nan
    
    ratings_user1 = merged_ratings['rating_x']
    ratings_user2 = merged_ratings['rating_y']
    mean_user1 = ratings_user1.mean() #mean of ratings of user1
    mean_user2 = ratings_user2.mean() #mean of ratings of user2
    
    num = np.sum((ratings_user1 - mean_user1)*(ratings_user2 - mean_user2))
    den = np.sqrt(np.sum((ratings_user1 - mean_user1)**2)) * np.sqrt(np.sum((ratings_user2 - mean_user2)**2))
    try:
        coef = num/den
    except (RuntimeWarning, ZeroDivisionError):
        return math.nan
    
    return coef

def prediction(userId, top10, movieId, ratings): #prediction function
    df_userA = ratings[ratings['userId'] == userId]
    userA_mean = df_userA['rating'].mean()
    users_for_film = ratings[ratings['movieId'] == movieId].drop(['movieId', 'rating'], axis = 1) #users that rated a specific film
    merged_users = set(users_for_film['userId']) & top10.keys() #get the users in top10 that rated the film in input
            
    num = 0
    den = 0
    if bool(set):
        for user in merged_users:
            df_userB = ratings[ratings['userId'] == user]
            sim = top10.get(user) #get pearson correlation value between the users
            if not math.isnan(sim):
                num += sim * (df_userB[df_userB['movieId'] == movieId].iloc[0]['rating'] - df_userB['rating'].mean())
                den += sim

        try:
            div = num/den
            pred = userA_mean + div
        except (RuntimeWarning, ZeroDivisionError):
            return math.nan
    else:
        return math.nan
    
    return pred

def get_single_similarity(userB, userA_ratings, ratings, dict, function):
    userB_ratings = get_usr_rows(ratings, 'userId', userB)
    
    #pearson correlation
    if function == 'pc':
        sim = pearson_correlation(userA_ratings, userB_ratings) #calculate pearson correlation value between the users
        if not math.isnan(sim):
            dict.update({userB : sim}) #add the user and the related pearson correlation value
    
    #jaccard similarity
    elif function == 'js':
        sim = jaccard_similarity(userA_ratings, userB_ratings)
        if not math.isnan(sim):
            dict.update({userB : sim})

    #cosine similarity
    elif function == 'cs':
        sim = cosine_similarity(userA_ratings, userB_ratings)
        if not math.isnan(sim):
            dict.update({userB : sim})

    #euclidean distance
    elif function == 'ed':
        sim = euclidean_distance_similarity(userA_ratings, userB_ratings)
        if not math.isnan(sim):
            dict.update({userB : sim})

def get_all_similarities(userA, userA_ratings, ratings, users, dict, function):
    pd.DataFrame.from_dict(users).map(lambda x: get_single_similarity(x, userA_ratings, ratings, dict, function) if(x != userA) else None) #call the function of similarity on every user

def get_single_prediction(userA, ratings, movie, movies, top10usr, dict):
    prd = prediction(userA, top10usr, movie, ratings) #calculate prediction on a specific movie
    if not math.isnan(prd):
        dict.update({movies[movies['movieId'] == movie].iloc[0]['title'] : prd}) #add the film title and the prediction to the dict

def get_all_predictions(userA, ratings, movies, column, top10usr, dict):
    movies[column].map(lambda x: get_single_prediction(userA, ratings, x, movies, top10usr, dict))

def get_top10(map):
    return dict(sorted(map.items(), key=lambda x:x[1], reverse=True)[:10])