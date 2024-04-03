import sys
import warnings
import utils
sys.path.append("../ass-01")
import ass01
import ass02

warnings.filterwarnings("error")

args = utils.parser()

USERS = args.users

while len(USERS) < 2:
    print(f'This user does not exist. Pick an Id in range(1, 610)')
    USERS.append(int(input()))

ratings, movies = ass01.read("../dataset/ratings.csv", "../dataset/movies.csv") #read csv files necessary
pred_mvs, sim_users = ass02.get_predicted_mvs(USERS, ratings, movies, args.function)

if args.method == 'avg':
    pred_mvs = ass02.avg_method(USERS, pred_mvs, sim_users, ratings) #get group recommendations with Average method
    top10mvs = ass01.get_top10(pred_mvs) #sort the output and get the top10
elif args.method == 'lm':
    pred_mvs = ass02.least_misery_method(USERS, pred_mvs, sim_users, ratings) #get group recommendations with Least Misery method
    top10mvs = ass01.get_top10(pred_mvs) #sort the output and get the top10
elif args.method == 'msd':
    pred_mvs = ass02.mean_squared_deviation_method(USERS, pred_mvs, sim_users, ratings) #get group recommendations with Mean Squared Deviation method
    top10mvs = ass02.get_top10(pred_mvs) #sort the output and get the top10

print(f'Top 10 films to suggest to users {USERS} in input with {args.method} method and {args.function} similarity function are {ass02.get_titles(top10mvs, movies)}')


