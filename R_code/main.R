library(GA);
source("functions.R");
source("tests.R");

data <- read.table("data/delavnice.csv", sep=",", header=T);
activities <- create_activities_vector(data);
participants <- create_participants_vector(data);
mapping_matrix <- create_mapping_matrix(participants, activities, data);

#age weight - how much does the same age matter
age_weight = 1;
#num_weight - how much do evenly assigned groups matter
num_weight = 0.5;
#
n_iter = 50;
p_cross = 0.7;
p_mut = 0.7;
selected_monitor = plot; #gaMonitor, plot
selected_selection=ga_nlrSelection #seems best so far

#Run GA
GA <- ga(type="binary", fitness=my_fitness_function1, nBits=get_nBits(mapping_matrix), population=my_init_pop, selection=selected_selection, crossover=my_crossover, mutation=my_mutation, pcrossover=p_cross, pmutation=p_mut, maxiter=n_iter, monitor=selected_monitor);

#Test results
