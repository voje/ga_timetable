library(GA);
source("functions.R");

data <- read.table("data/delavnice.csv", sep=",", header=T);
activities <- create_activities_vector(data);
participants <- create_participants_vector(data);
mapping_matrix <- create_mapping_matrix(participants, activities, data);

GA <- ga(type="binary", fitness=my_fitness_function, nBits=get_nBits(mapping_matrix), population=my_init_pop, maxiter=20);

