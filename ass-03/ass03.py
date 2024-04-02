import sys
import numpy as np
sys.path.append("../ass-01")
import ass01
sys.path.append("../ass-02")
import ass02

def get_sorted_column(df):
    return df.sort_values(ascending=False)

def get_first_nrows(df, n):
    return df.head(n)

def get_topN(map, n):
    return dict(sorted(map.items(), key=lambda x:x[1], reverse=True)[:n])

def alpha_update(user_sat):
    return max(user_sat.values()) - min(user_sat.values())

def seq_hybrid_aggregation(alpha, avg, lm):
    return ((1 - alpha) * avg) + (alpha * lm)

def get_avg_lm(users, similar_users, movie, pred_movies, ratings):
    return (ass02.avg_function(users, similar_users, movie, pred_movies, ratings), ass02.least_misery_function(users, similar_users, movie, pred_movies, ratings))

def user_satisfaction(users, pred_movies, last_mvs, ratings):
    usr_sat = dict()
    n = len(last_mvs)
    for user in users:
        num = 0
        den = np.sum(get_first_nrows(get_sorted_column(ass01.get_column(ass01.get_usr_rows(ratings, 'userId', user), 'rating')), n))
        for movie in last_mvs.keys():
            num += pred_movies[movie][user]

        sat = num/den
        usr_sat[user] = sat
    
    return usr_sat

def sequential_recommendation(iterations, mvs_number, users, pred_movies, similar_users, ratings):
    alpha = 0 #alpha parameter
    output_mvs = dict() #this will be the output of the group recommendation
    
    avg_lm_mvs = dict() #dict to 
    for i in range(iterations):
        seq_mvs = dict()
        if i > 0:
            user_sat = user_satisfaction(users, pred_movies, output_mvs, ratings)
            alpha = alpha_update(user_sat)
        
        mvs_keys = pred_movies.keys() - output_mvs.keys()
        for movie in mvs_keys:   
            if i == 0:
                avg, lm = get_avg_lm(users, similar_users, movie, pred_movies, ratings)
                avg_lm_mvs[movie] = {'avg' : avg, 'lm' : lm}
            
            seq_value = seq_hybrid_aggregation(alpha, avg_lm_mvs[movie]['avg'], avg_lm_mvs[movie]['lm'])
            seq_mvs[movie] = seq_value

        if i == 2:
            n = (mvs_number//iterations) + 1
        else:
            n = mvs_number//iterations    
        
        seq_mvs = get_topN(seq_mvs, n)
        output_mvs.update(seq_mvs.copy())

    return output_mvs
