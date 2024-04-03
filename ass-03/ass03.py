import sys
import numpy as np
sys.path.append("../ass-01")
import ass01
sys.path.append("../ass-02")
import ass02

def get_sorted_column(df): #function to get the column with sorted values in ascending order
    return df.sort_values(ascending=False)

def get_first_nrows(df, n): #function to get first 'n' rows from dataframe
    return df.head(n)

def get_topN(map, n): #function to get  top 'n' elements from a dictionary by value
    return dict(sorted(map.items(), key=lambda x:x[1], reverse=True)[:n])

def alpha_update(user_sat): #function to update alpha parameter based on users satisfaction
    return max(user_sat.values()) - min(user_sat.values())

def seq_hybrid_aggregation(alpha, avg, lm): #function of hybrid aggregation of sequential recommendations
    return ((1 - alpha) * avg) + (alpha * lm)

def seq_hybrid_msd_aggregation(alpha, avg, lm, msd): #function of hybrid MSD aggregation of sequential recommend
    return ((1 - alpha) * avg) + (alpha * lm) + (alpha * msd)

def get_avg_lm(users, similar_users, movie, pred_movies, ratings): #function to get average and minimum prediction for a group of users on a specific movie
    return (ass02.avg_function(users, similar_users, movie, pred_movies, ratings), ass02.least_misery_function(users, similar_users, movie, pred_movies, ratings))

def user_satisfaction(users, pred_movies, last_mvs, ratings): #function to calculate user satisfaction of the previous iteration
    usr_sat = dict()
    n = len(last_mvs) #number of movies predicted sequentially from previous iterations
    for user in users:
        num = 0 #numerator
        den = np.sum(get_first_nrows(get_sorted_column(ass01.get_column(ass01.get_usr_rows(ratings, 'userId', user), 'rating')), n)) #get the first n rows of sorted user ratings
        for movie in last_mvs.keys():
            num += pred_movies[movie][user] #update numerator with prediction for each movie

        sat = num/den
        usr_sat[user] = sat #store user satisfaction level
    
    return usr_sat

def sequential_recommendation(iterations, mvs_number, users, pred_movies, similar_users, ratings):
    alpha = 0 #alpha parameter
    output_mvs = dict() #this will be the output of the group recommendation
    
    avg_lm_mvs = dict() #dict to store avg and minimimum prediction score for each movie
    for i in range(iterations):
        seq_mvs = dict() #dict to store movies recommended in a single interation
        if i > 0:
            user_sat = user_satisfaction(users, pred_movies, output_mvs, ratings) #update user satisfaction based on current predictions
            alpha = alpha_update(user_sat) #update alpha parameter
        
        mvs_keys = pred_movies.keys() - output_mvs.keys() #update mvs that have not been recommended yet
        for movie in mvs_keys:   
            if i == 0: #at the first iteration
                avg, lm = get_avg_lm(users, similar_users, movie, pred_movies, ratings) #calculate avg and minimimum prediction score for each movie
                avg_lm_mvs[movie] = {'avg' : avg, 'lm' : lm} #store these values 
            
            seq_value = seq_hybrid_aggregation(alpha, avg_lm_mvs[movie]['avg'], avg_lm_mvs[movie]['lm']) #get sequential value based on hybrid aggregation formula
            seq_mvs[movie] = seq_value #update the sequential value on each movie

        if i == 2: #hardcoded 
            n = (mvs_number//iterations) + 1 #hardcoded output
        else:
            n = mvs_number//iterations #hardcoded output
        
        seq_mvs = get_topN(seq_mvs, n) #get top n movies recommendation of the iteration
        output_mvs.update(seq_mvs.copy()) #update the output dict

    return output_mvs

def sequential_msd_recommendation(iterations, mvs_number, users, pred_movies, similar_users, ratings):
    alpha = 0 #alpha parameter
    output_mvs = dict() #this will be the output of the group recommendation
    
    avg_lm_msd_mvs = dict() #dict to store avg, minimimum prediction score and MSD on scores for each movie
    for i in range(iterations):
        seq_mvs = dict() #dict to store movies recommended in a single interation
        if i > 0:
            user_sat = user_satisfaction(users, pred_movies, output_mvs, ratings) #update user satisfaction based on current predictions
            alpha = alpha_update(user_sat) #update alpha parameter
        
        mvs_keys = pred_movies.keys() - output_mvs.keys() #update mvs that have not been recommended yet
        for movie in mvs_keys:   
            if i == 0:
                avg, lm = get_avg_lm(users, similar_users, movie, pred_movies, ratings) #calculate avg and minimimum prediction score for each movie
                msd = np.sqrt((np.sum(np.array(list(dict(pred_movies[movie]).values())) - avg)**2)/len(users)) #calculate MSD on prediction scores for each movie
                avg_lm_msd_mvs[movie] = {'avg' : avg, 'lm' : lm, 'msd' : msd} #store these values
            
            seq_value = seq_hybrid_msd_aggregation(alpha, avg_lm_msd_mvs[movie]['avg'], avg_lm_msd_mvs[movie]['lm'], avg_lm_msd_mvs[movie]['msd']) #get sequential value based on hybrid aggregation + MSD formula
            seq_mvs[movie] = seq_value #update the sequential value on each movie

        if i == 2: #hardcoded 
            n = (mvs_number//iterations) + 1 #hardcoded output
        else:
            n = mvs_number//iterations #hardcoded output
        
        seq_mvs = get_topN(seq_mvs, n) #get top n movies recommendation of the iteration
        output_mvs.update(seq_mvs.copy()) #update the output dict

    return output_mvs
