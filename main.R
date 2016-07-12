library(GA);
source("functions.R");

data <- read.table("data/delavnice.csv", sep=",", header=T);
activities <- create_activities_vector(data);
participants <- create_participants_vector(data);
mapping_matrix <- create_mapping_matrix(participants, activities, data);

#age weight - how much does the same age matter
age_weight = 1;
#num_weight - how much do evenly assigned groups matter
num_weight = 0.5;
#
n_iter = 400;
GA <- ga(type="binary", fitness=my_fitness_function, nBits=get_nBits(mapping_matrix), population=my_init_pop, maxiter=n_iter);

pretty <- pretty_table(GA@solution);

