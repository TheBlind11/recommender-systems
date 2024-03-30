import sys
import warnings
sys.path.append("../ass-01")
import ass01
import ass02

warnings.filterwarnings("error")

USERS = []
for i in range(1, len(sys.argv)):
    USERS.append(int(sys.argv[i]))

ratings, movies = ass01.read("../dataset/ratings.csv", "../dataset/movies.csv") #read csv files necessary
all_mvs, all_users = ass02.get_predicted_mvs(USERS, ratings, movies)
all_mvs2 = all_mvs
#all_mvs = ass02.avg_method(USERS, all_mvs, all_users, ratings)

all_mvs2 = ass02.least_misery_method(USERS, all_mvs2, all_users, ratings)
print(all_mvs2)


