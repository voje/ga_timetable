source("functions.R");

data <- read.table("data/delavnice.csv", sep=",", header=T);
activities <- create_activities_vector(data);
participants <- create_participants_vector(data);
mm <- create_mapping_matrix(participants, activities, data);

