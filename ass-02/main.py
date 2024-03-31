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
all_mvs, all_users = ass02.get_predicted_mvs(USERS, ratings, movies, args.function)

if args.method == 'avg':
    all_mvs = ass02.avg_method(USERS, all_mvs, all_users, ratings)
    top10mvs = ass01.get_top10(all_mvs)
elif args.method == 'lm':
    all_mvs = ass02.least_misery_method(USERS, all_mvs, all_users, ratings)
    top10mvs = ass01.get_top10(all_mvs)
elif args.method == 'msd':
    all_mvs = ass02.mean_squared_deviation_method(USERS, all_mvs, all_users, ratings)
    top10mvs = ass02.get_top10(all_mvs)

print(f'Top 10 films to suggest to users {USERS} in input with {args.method} method are {ass02.get_titles(top10mvs, movies)}')


