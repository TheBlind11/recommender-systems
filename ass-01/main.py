import warnings
import utils
import ass01

warnings.filterwarnings("error")

args = utils.parser()

USER_A = args.user
while USER_A == None or USER_A <= 0 or USER_A > 610:
    print(f'This user does not exist. Pick an Id in range(1, 610)')
    USER_A = int(input())

ratings, movies = ass01.read("../dataset/ratings.csv", "../dataset/movies.csv") #read csv files necessary

USER_A_ratings = ass01.get_usr_rows(ratings, 'userId', USER_A)
USER_A_films = ass01.get_column(USER_A_ratings, 'movieId')

#rows_count = len(ratings) #number of rows
#print(f'ratings.csv has {rows_count} rows. ') #check number of rows

users = ass01.get_all_users(ratings) #all the users of the dataset
topusers = dict() #all the similarities between user in input and other users
ass01.get_all_similarities(USER_A, USER_A_ratings, ratings, users, topusers, args.function) #get the similarity on every user
top10usr = ass01.get_top10(topusers) #get top 10 users similar to user in input
print(f'Top 10 users similar to user {USER_A} are {top10usr}')    

mvs = ass01.get_df_difference(movies, USER_A_films) #get movies not rated by user
mvs_sugg = dict() #movies to sugget to user in input
ass01.get_all_predictions(USER_A, ratings, mvs, 'movieId', top10usr, mvs_sugg) #get the prediction on every movie not rated by user
top10mvs = ass01.get_top10(mvs_sugg) #get top 10 films to suggest to user in input
print(f'Top 10 films to suggest to user {USER_A} in input are {top10mvs}')