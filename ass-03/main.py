import sys
import warnings
import utils
sys.path.append("../ass-01")
import ass01
sys.path.append("../ass-02")
import ass02
import ass03

warnings.filterwarnings("error")

args = utils.parser()

USERS = args.users
N_ITERATIONS = 3
N_FILMS = 10

while len(USERS) < 2:
    print(f'This user does not exist. Pick an Id in range(1, 610)')
    USERS.append(int(input()))

ratings, movies = ass01.read("../dataset/ratings.csv", "../dataset/movies.csv") #read csv files necessary
pred_mvs, sim_users = ass02.get_predicted_mvs(USERS, ratings, movies, args.function)

if args.method == 'seq':
    seq_mvs = ass03.sequential_recommendation(N_ITERATIONS, N_FILMS, USERS, pred_mvs, sim_users, ratings) #get sequential recommendations with Hybrid Aggregation Model
elif args.method == 'msd':
    seq_mvs = ass03.sequential_msd_recommendation(N_ITERATIONS, N_FILMS, USERS, pred_mvs, sim_users, ratings) #get sequential recommendations with Hybrid Aggregation + MSD Model

print(f'Top 10 films to suggest to users {USERS} in input with {args.method} method and {args.function} similarity function are {ass02.get_titles(seq_mvs, movies)}')



